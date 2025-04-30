from src.google_meet.auth import GoogleAuth
from google.apps import meet_v2 as meet

class GoogleSpace():
    def __init__(self):
        self.creds = None
        self.space = None

    def create_space(self):
        """Create a meeting space."""
        auth = GoogleAuth()
        auth.set_credentials()
        self.creds = auth.creds
        client = meet.SpacesServiceClient(credentials=self.creds)
        request = meet.CreateSpaceRequest()
        self.space = client.create_space(request=request)