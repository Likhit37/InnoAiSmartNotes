"""
Protected route example.
Demonstrates JWT authentication and MongoDB-safe serialization.
"""

from fastapi import APIRouter, Depends
from bson import ObjectId

# ✅ Correct import location
from backend.shared.core.dependencies import get_current_user


router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)


def serialize_mongo_document(doc: dict) -> dict:
    """
    Convert MongoDB ObjectId to string
    so FastAPI can serialize it properly.
    """
    if not doc:
        return doc

    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])

    return doc


@router.get("/")
def protected_route(current_user: dict = Depends(get_current_user)):
    """
    Example protected endpoint.
    Requires valid JWT.
    """

    user = serialize_mongo_document(current_user)

    return {
        "message": "You are authenticated",
        "user": user
    }
