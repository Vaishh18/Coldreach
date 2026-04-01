import sqlite3

DB = "emails.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            thread_id TEXT UNIQUE NOT NULL,
            gmail_msg_id TEXT,
            subject TEXT,
            replied INTEGER DEFAULT 0,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            replied_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_sent_email(email, thread_id, gmail_msg_id, subject):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO emails (email, thread_id, gmail_msg_id, subject, replied)
        VALUES (?, ?, ?, ?, 0)
    """, (email, thread_id, gmail_msg_id, subject))
    conn.commit()
    conn.close()

def mark_replied(thread_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        UPDATE emails
        SET replied = 1, replied_at = CURRENT_TIMESTAMP
        WHERE thread_id = ?
    """, (thread_id,))
    conn.commit()
    conn.close()