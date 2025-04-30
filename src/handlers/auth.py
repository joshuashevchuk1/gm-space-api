# handlers/auth.py

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from src.google_meet.auth import GoogleAuth

router = APIRouter()

@router.get(
    "/auth",
    response_class=PlainTextResponse,
    tags=["auth"],
    summary="auth",
    description="gets a token for authentication into google meetsE",
    responses={200: {"description": "Google auth passed"}},
)

def auth():
    googleAuth = GoogleAuth()
    googleAuth.set_credentials()
