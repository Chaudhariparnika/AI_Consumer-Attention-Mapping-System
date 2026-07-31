from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database.database import SessionLocal, get_db
from app.auth import SECRET_KEY, ALGORITHM
from app import model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> model.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(model.User).filter(model.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user: model.User = Depends(get_current_user)) -> model.User:
    """Enforces Admin-only access guard"""
    if current_user.role != model.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Admin role required for this action."
        )
    return current_user


def require_store_manager(current_user: model.User = Depends(get_current_user)) -> model.User:
    """Allow store managers and admins to access store-level metrics."""
    if current_user.role not in {model.UserRole.STORE_MANAGER, model.UserRole.ADMIN}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Store manager role required for this action."
        )
    return current_user