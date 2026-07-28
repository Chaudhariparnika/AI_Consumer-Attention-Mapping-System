from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import Base, engine, SessionLocal, get_db
from app.model import User
from app.schema import LoginUser , LoginAdmin
from app.auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }






