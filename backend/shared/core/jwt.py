"""
JWT utility functions.

Responsible for:
- Creating access tokens
- Managing expiration
"""

from datetime import datetime, timedelta
from jose import jwt

from backend.shared.core.config import settings


def create_access_token(data: dict) -> str:
    """
    Generate a signed JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt
