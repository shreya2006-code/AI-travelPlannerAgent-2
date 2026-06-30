from fastapi import APIRouter
from pydantic import BaseModel

from app.core.agent import planner

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str

class ResetRequest(BaseModel):
    session_id: str


@router.post("/chat")
def chat(request: ChatRequest):

    result = planner.generate_trip(
        request.session_id,
        request.message
    )

    if not result.get("success", True):
        return {
            "success": False,
            "session_id": request.session_id,
            "message": result.get(
                "message",
                "Something went wrong."
            ),
            "itinerary": None,
            "trip": None
        }

    return {
        "success": True,
        "session_id": request.session_id,
        "message": "Trip generated successfully.",

        "chat_response": result["chat_response"],

        "itinerary": result["itinerary"],

        "trip": result["trip"]
    }

@router.post("/reset-session")
def reset_session(request: ResetRequest):

    return planner.reset_session(
        request.session_id
    )