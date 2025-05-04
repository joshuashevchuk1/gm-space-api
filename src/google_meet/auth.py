# handlers/auth.py

from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleAuth():
    def __init__(self):
        self.creds = None
        self.base_api_url = None

    def set_credentials(self):
        """Ensure valid credentials for calling the Meet REST API."""
        CLIENT_SECRET_FILE = "./oauth.json"

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
            self.creds.refresh(google_requests.Request())
