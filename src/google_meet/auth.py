# handlers/auth.py

import os
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class GoogleAuth():
    def __init__(self):
        self.creds = None

    def set_credentials(self):
        """Ensure valid credentials for calling the Meet REST API."""
        CLIENT_SECRET_FILE = "./oauth.json"

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json')

        if self.creds is None:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE,
                scopes=[
                    'https://www.googleapis.com/auth/meetings.space.created',
                    'https://www.googleapis.com/auth/drive.readonly',
                ])
            flow.run_local_server(port=0)
            self.creds = flow.credentials

        if self.creds and self.creds.expired:
            self.creds.refresh(requests.Request())

        if self.creds is not None:
            with open("token.json", "w") as f:
                f.write(self.creds.to_json())
