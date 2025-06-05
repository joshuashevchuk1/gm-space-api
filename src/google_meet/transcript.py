import re

import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import io
import os
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/meetings.space.created','https://www.googleapis.com/auth/drive.readonly']

class GoogleTranscript():
    def __init__(self):
        self.creds = None
        self.url = None
        self.file_id = None

    def _post_transcript(self, meet_key, file_path):
        url = f"http://localhost:8080/{meet_key}/transcript"

        # Metadata to send as form fields
        data = {
            "meet_key": self.meet_key,
            "space_name": self.space_name,
            "space_uri": self.space_uri,
        }

        # Open the file you want to upload
        with open(file_path, 'rb') as f:
            files = {
                "file": (file_path, f, "application/octet-stream")  # adjust MIME type as needed
            }

            response = requests.post(url, data=data, files=files)

        return response

    def upload_google_doc(self, google_doc):
        self.file_id = self._parse_transcript_id()


    def download_transcript(self, export_mime='application/pdf', output_file='output.pdf'):
        output_file = 'output.pdf'
        self.file_id = self._parse_transcript_id()

        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                'oauth.json', SCOPES)
            creds = flow.run_local_server(port=0)

        if creds is not None:
            with open("token.json", "w") as f:
                f.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        request = service.files().export_media(fileId=self.file_id,
                                               mimeType=export_mime)

        fh = io.FileIO(output_file, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        print(f"Downloaded '{output_file}' successfully.")
        return output_file


    def _parse_transcript_id(self):
        match = re.search(r"/d/([^/]+)", self.url)
        transcript_id = None
        if match:
            transcript_id = match.group(1)
            print("Transcript ID:", transcript_id)
        else:
            print("Transcript ID not found.")
        return transcript_id

    def upload_transcript(self):
        return