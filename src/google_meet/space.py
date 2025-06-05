import requests

from src.config import config
from src.google_meet.auth import GoogleAuth
from google.apps import meet_v2 as meet

class GoogleSpace():
    def __init__(self):
        self.creds = None
        self.space = None
        self.space_name = None
        self.space_uri = None
        self.meet_key = None
        self.config = config.Config()

    def create_space(self):
        auth = GoogleAuth()
        auth.set_credentials()
        self.creds = auth.creds
        client = meet.SpacesServiceClient(credentials=self.creds)
        request = meet.CreateSpaceRequest()
        self.space = client.create_space(request=request)
        self.space_name = self.space.name
        self.space_uri = self.space.meeting_uri
        self.meet_key = self.space.meeting_code
        response = self._post_space()
        return response

    def _post_space(self):
        url = "http://localhost:8080/document"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "meet_key": self.meet_key,
            "space_name": self.space_name,
            "space_uri": self.space_uri,
        }

        response = requests.post(url, headers=headers, json=data)
        return response