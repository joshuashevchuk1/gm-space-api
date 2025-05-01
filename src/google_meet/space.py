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

    class GoogleSession():
        def __init__(self):
            self.creds = None
            self.space_name = None
            self.topic_name = None

        def subscribe_to_space(self, space_name: str = None, topic_name: str = None):
            """Subscribe to events for a meeting space."""
            session = requests.AuthorizedSession(self.creds)
            body = {
                'targetResource': f"//meet.googleapis.com/{space_name}",
                "eventTypes": [
                    "google.workspace.meet.conference.v2.started",
                    "google.workspace.meet.conference.v2.ended",
                    "google.workspace.meet.participant.v2.joined",
                    "google.workspace.meet.participant.v2.left",
                    "google.workspace.meet.recording.v2.fileGenerated",
                    "google.workspace.meet.transcript.v2.fileGenerated",
                ],
                "payloadOptions": {
                    "includeResource": False,
                },
                "notificationEndpoint": {
                    "pubsubTopic": topic_name
                },
                "ttl": "86400s",
            }
            response = session.post("https://workspaceevents.googleapis.com/v1/subscriptions", json=body)
            if response.status_code == 403:
                raise Exception("got 403 : ", str(response.content))
            return response