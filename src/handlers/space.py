# handlers/auth.py

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from src.google_meet.space import GoogleSpace

router = APIRouter()

@router.get(
    "/space",
    response_class=PlainTextResponse,
    tags=["space"],
    summary="space",
    description="gets a uri for google spaces",
    responses={200: {"description": "Google Space created"}},
)

def create_space():
    googleSpace = GoogleSpace()
    response = googleSpace.create_space()
    print("response : ", str(response))