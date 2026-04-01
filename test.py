import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.utils import make_msgid

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

creds = Credentials.from_authorized_user_file("token.json",SCOPES)
service  = build("gmail","v1",credentials=creds)

message = EmailMessage()
message.set_content("Hello Vaishnavi, this is your first API email 🚀")
message["To"] = "vaishnavipati90@gmail.com"
message["From"] = "vaishnavipati90@gmail.com"
message["Subject"] = "Test Email"
encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

send_message = service.users().messages().send(
    userId = "me",
    body = {"raw":encoded_message}
).execute()

print("Email sent! ID:",send_message["id"])
