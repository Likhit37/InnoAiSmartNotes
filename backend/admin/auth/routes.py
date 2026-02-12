from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.shared.db.mongo import mongodb
from backend.shared.core.security import verify_password
from backend.shared.core.jwt import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = mongodb.db.users.find_one({"email": form_data.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user["_id"]),
            "role": user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
