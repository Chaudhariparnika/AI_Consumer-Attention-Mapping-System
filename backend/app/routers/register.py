from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from app.schema import RegisterUser, UserResponse 
from app.model import User
from app.auth import hash_password

router = APIRouter(
    prefix="/api",
    tags=["Register"]
)

#user registration endpoint
@router.post("/register", response_model=UserResponse)
def register_user(user: RegisterUser, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user