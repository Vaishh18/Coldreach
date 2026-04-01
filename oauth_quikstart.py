# oauth_quickstart.py
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify"
]

def main():
    creds_path = Path("token.json")
    creds = None
    if creds_path.exists():
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    print("Got token.json — mailbox labels:", [l["name"] for l in labels])

if __name__ == "__main__":
    main()