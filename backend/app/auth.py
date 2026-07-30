from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from typing import Optional


# Secret Key (Change this in production)
SECRET_KEY = "your_secret_key_here"

# JWT Algorithm
ALGORITHM = "HS256"

# Token Expiry Time (Minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing Context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Password Functions

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# JWT Token Functions

def create_access_token(data: dict):
    """
    Creates a JWT access token.

    Example payload:
    {
        "id": 1,
        "email": "abc@gmail.com",
        "role": "admin"
    }
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str):
    """
    Decodes JWT token and returns payload.
    Returns None if token is invalid or expired.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None
    


SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_GLASSMORPHISM_KEY_CHANGE_IN_PROD")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)