from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime

from backend.shared.db.mongo import mongodb
from backend.admin.users.schemas import UserCreate
from backend.shared.core.security import hash_password
from backend.shared.core.dependencies import require_admin


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", dependencies=[Depends(require_admin)])
def create_user(user: UserCreate):
    # Check if email already exists
    if mongodb.db.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["created_at"] = datetime.utcnow()

    result = mongodb.db.users.insert_one(user_dict)

    return {
        "message": "User created successfully",
        "user_id": str(result.inserted_id)
    }


@router.get("/", dependencies=[Depends(require_admin)])
def list_users():
    users = list(mongodb.db.users.find())

    for user in users:
        user["id"] = str(user["_id"])
        user.pop("_id", None)
        user.pop("password", None)

    return users
