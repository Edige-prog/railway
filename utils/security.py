from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, WebSocket, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "TOP_SECRET111"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


class CookieOrHeaderTokenScheme(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        # First try to get the token from the header
        header_token = await super().__call__(request)
        if header_token:
            return header_token

        # If no header token, try to get it from the cookie
        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            return cookie_token

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Create the scheme instance
oauth2_scheme = CookieOrHeaderTokenScheme(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """Hash the user's password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the hashed password matches the plain password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(user_id: int) -> str:
    """Create a JWT token for the given user ID."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str) -> int:
    """Decode the JWT token and extract the user ID."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise JWTError("Invalid token")
        return user_id
    except JWTError as e:
        raise e