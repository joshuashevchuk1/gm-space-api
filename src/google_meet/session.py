import threading
import traceback

from google.auth.transport import requests as google_requests
from google.apps import meet_v2 as meet
from google.apps import meet
from google.cloud import pubsub_v1
import json

from src.config import config
from src.google_meet.space import GoogleSpace


class GoogleSession():
    def __init__(self):
        self.creds = None
        self.space_name = None
        self.config = config.Config()
        self.topic_name = self.config.get_g_meet_topic_name()
        self.subscription_name = self.config.get_g_meet_subscription_name()

    def _subscribe_to_space(self):
        """Subscribe to events for a meeting space."""
        session = google_requests.AuthorizedSession(self.creds)
        body = {
            'targetResource': f"//meet.googleapis.com/{self.space_name}",
            "eventTypes": [
                "google.workspace.meet.conference.v2.started",
                "google.workspace.meet.conference.v2.ended",
                "google.workspace.meet.recording.v2.fileGenerated",
                "google.workspace.meet.transcript.v2.fileGenerated",
            ],
            "payloadOptions": {
                "includeResource": False,
            },
            "notificationEndpoint": {
                "pubsubTopic": self.topic_name
            },
            "ttl": "86400s",
        }
        response = session.post("https://workspaceevents.googleapis.com/v1/subscriptions", json=body)
        if response.status_code == 403:
            raise Exception("got 403 : ", str(response.content))

    def on_conference_started(self, message: pubsub_v1.subscriber.message.Message):
        """Display information about a conference when started."""
        payload = json.loads(message.data)
        resource_name = payload.get("conferenceRecord").get("name")
        client = meet.ConferenceRecordsServiceClient(credentials=self.creds)
        conference = client.get_conference_record(name=resource_name)
        print(f"Conference (ID {conference.name}) started at {conference.start_time.rfc3339()}")

    def on_conference_ended(self, message: pubsub_v1.subscriber.message.Message):
        """Display information about a conference when ended."""
        payload = json.loads(message.data)
        resource_name = payload.get("conferenceRecord").get("name")
        client = meet.ConferenceRecordsServiceClient(credentials=self.creds)
        conference = client.get_conference_record(name=resource_name)
        print(f"Conference (ID {conference.name}) ended at {conference.end_time.rfc3339()}")

    def on_recording_ready(self, message: pubsub_v1.subscriber.message.Message):
        """Display information about a recorded meeting when artifact is ready."""
        payload = json.loads(message.data)
        resource_name = payload.get("recording").get("name")
        client = meet.ConferenceRecordsServiceClient(credentials=self.creds)
        recording = client.get_recording(name=resource_name)
        print(f"Recording available at {recording.drive_destination.export_uri}")

    def on_transcript_ready(self, message: pubsub_v1.subscriber.message.Message):
        """Display information about a meeting transcript when artifact is ready."""
        payload = json.loads(message.data)
        resource_name = payload.get("transcript").get("name")
        transcript_id = resource_name.split('/')[-1]

        client = meet.ConferenceRecordsServiceClient(credentials=self.creds)
        transcript = client.get_transcript(name=resource_name)

        print("transcript payload is:", str(payload))
        print("transcript is:", transcript.name)
        print("Transcript ID:", transcript_id)
        print(f"Transcript available at {transcript.docs_destination.export_uri}")

    def on_message(self, message: pubsub_v1.subscriber.message.Message) -> None:
        """Handles an incoming event from the Google Cloud Pub/Sub API."""
        event_type = message.attributes.get("ce-type")
        handler = {
            "google.workspace.meet.conference.v2.started":self.on_conference_started,
            "google.workspace.meet.conference.v2.ended": self.on_conference_ended,
            "google.workspace.meet.recording.v2.fileGenerated": self.on_recording_ready,
            "google.workspace.meet.transcript.v2.fileGenerated": self.on_transcript_ready,
        }.get(event_type)

        try:
            if handler is not None:
                handler(message)
            message.ack()
        except Exception as error:
            print("Unable to process event")
            print(error)

    def listen_for_events(self):
        """Blocking listener that runs in a background thread."""
        subscriber = pubsub_v1.SubscriberClient()
        with subscriber:
            future = subscriber.subscribe(self.subscription_name, callback=self.on_message)
            print("Listening for events...")
            future.result()  # This blocks, but it's okay in a background thread

    def _create_space(self):
        print('entering _create_space')
        googleSpace = GoogleSpace()
        try:
            response = googleSpace.create_space()
            print("response : ", str(response))
            self.creds = googleSpace.creds
            self.space_name = googleSpace.space_name
            print(f"{googleSpace.space_uri}")
            print(f"{googleSpace.space_name}")
            print('leaving _create_space')
        except:
            traceback.print_exc()

    def start_session(self):
        """Run the listener in a background thread so it doesn't block the main app."""
        self._create_space()
        self._subscribe_to_space()
        listener_thread = threading.Thread(target=self.listen_for_events, daemon=True)
        listener_thread.start()
