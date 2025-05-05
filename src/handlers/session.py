# handlers/auth.py

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.google_meet.session import GoogleSession
from src.google_meet.space import GoogleSpace

router = APIRouter()

@router.get(
    "/session",
    response_class=PlainTextResponse,
    tags=["session"],
    summary="session",
    description="starts a google session",
    responses={200: {"description": "Google Space Session started"}},
)

def start_google_session():
    googleSession = GoogleSession()
    googleSession.start_session()