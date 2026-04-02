import base64
import csv
import io
from email.message import EmailMessage

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from auth import get_gmail_creds

from db import init_db, save_sent_email

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    creds = get_gmail_creds()
    return build("gmail", "v1", credentials=creds)


init_db()


def send_one(to_email, subject, body_text):
    service = get_gmail_service()

    message = EmailMessage()
    message["To"] = to_email
    message["From"] = "vaishnavipati90@gmail.com"
    message["Subject"] = subject
    message.set_content(body_text)

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()

    gmail_msg_id = sent["id"]
    thread_id = sent["threadId"]

    save_sent_email(to_email, thread_id, gmail_msg_id, subject)

    print("Sent:", to_email)
    print("Thread ID:", thread_id)


def build_body(name, company):
    return f"""HI {name},
I hope you are doing well. I wanted to reach out regarding a referral opportunity at {company}.

Best Wishes,
Vaishnavi
"""


def send_from_uploaded_csv(uploaded_file):
    uploaded_file.seek(0)
    csv_text = io.StringIO(uploaded_file.getvalue().decode("utf-8-sig"))
    reader = csv.DictReader(csv_text)

    for row in reader:
        name = row["name"].strip()
        email = row["email"].strip()
        company = row["company"].strip()

        subject = f"Referral request for {company}"
        body = build_body(name, company)

        send_one(email, subject, body)