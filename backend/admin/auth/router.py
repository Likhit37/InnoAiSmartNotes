"""
Authentication API routes.
"""

from fastapi import APIRouter

from backend.admin.auth.schemas import LoginRequest, TokenResponse
from backend.admin.auth.service import authenticate_user, generate_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Authenticate user and return JWT token.
    """

    user = authenticate_user(request.email, request.password)
    token = generate_token(user)

    return TokenResponse(access_token=token)
