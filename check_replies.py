import sqlite3
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from db import mark_replied
from telegram_notify import notify_telegram

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
DB = "emails.db"

def get_pending_threads():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT thread_id, email, subject FROM emails WHERE replied = 0")
    rows = cur.fetchall()
    conn.close()
    return {row[0]: {"email": row[1], "subject": row[2]} for row in rows}

def check_for_replies():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    pending = get_pending_threads()

    results = service.users().messages().list(
        userId="me",
        q="is:unread in:inbox",
        maxResults=10
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        print("No unread emails")
        return

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        thread_id = msg_data.get("threadId")
        snippet = msg_data.get("snippet", "")

        if "address not found" in snippet.lower() or "delivery status notification" in snippet.lower():
            print("Bounce detected, skipping")
            continue

        if thread_id in pending:
            print("Reply detected")
            mark_replied(thread_id)
            text = (
                f"Reply detected from {pending[thread_id]['email']}\n"
                f"Subject: {pending[thread_id]['subject']}\n"
                f"Snippet: {snippet}"
            )
            notify_telegram(text)
            print("Telegram alert sent")
        else:
            print("No match for this email")