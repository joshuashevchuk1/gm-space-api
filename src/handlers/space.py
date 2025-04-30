# handlers/auth.py

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import os
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

router = APIRouter()


@router.get(
    "/space",
    response_class=PlainTextResponse,
    tags=["space"],
    summary="makes a new google space",
    description="gets a token for authentication into google meetsE",
    responses={200: {"description": "Google auth passed"}},
)
def auth():
    handle_credentials()


def handle_credentials() -> Credentials:
    """Ensure valid credentials for calling the Meet REST API."""
    CLIENT_SECRET_FILE = "./oauth.json"
    credentials = None

    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json')

    if credentials is None:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=[
                'https://www.googleapis.com/auth/meetings.space.created',
                'https://www.googleapis.com/auth/drive.readonly',
            ])
        flow.run_local_server(port=0)
        credentials = flow.credentials

    if credentials and credentials.expired:
        credentials.refresh(requests.Request())

    if credentials is not None:
        with open("token.json", "w") as f:
            f.write(credentials.to_json())

    return credentials
