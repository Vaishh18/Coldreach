import streamlit as st
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify"
]

def get_gmail_creds():
    return Credentials(
        token=None,
        refresh_token=st.secrets["GMAIL_REFRESH_TOKEN"],
        token_uri=st.secrets["GMAIL_TOKEN_URI"],
        client_id=st.secrets["GMAIL_CLIENT_ID"],
        client_secret=st.secrets["GMAIL_CLIENT_SECRET"],
        scopes=SCOPES,
    )