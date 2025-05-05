import io
import re

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class GoogleTranscript():
    def __init__(self):
        self.creds = None
        self.url = None

    def download_google_doc(self, export_mime='application/pdf', output_file='output.pdf'):

        file_id = self._parse_transcript_id()

        service = build(
            'drive',
            'v3',
            credentials=self.creds)

        request = (service.
                   files().
                   export_media(
            fileId=file_id,
            mimeType=export_mime))

        fh = io.FileIO(output_file, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        print(f"Downloaded '{output_file}' successfully.")

    def _parse_transcript_id(self):
        match = re.search(r"/d/([^/]+)", self.url)
        transcript_id = None
        if match:
            transcript_id = match.group(1)
            print("Transcript ID:", transcript_id)
        else:
            print("Transcript ID not found.")
        return transcript_id
