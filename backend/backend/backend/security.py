from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Any
import os
from jose import JWTError, jwt

# English comments are used in the code as requested.

# --- Password Hashing ---

# Initialize the password hashing context.
# We are using bcrypt as the default hashing algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed one.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.
    """
    return pwd_context.hash(password)


# --- JWT Token Creation ---

# TODO: This should be loaded from environment variables, not hardcoded.
# You can generate a good secret key with: openssl rand -hex 32
SECRET_KEY = "a_very_secret_key_that_should_be_changed"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a new JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict[str, Any]:
    """
    Dekodiert einen JWT Access Token und gibt die enthaltenen Daten zurück.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return {}
