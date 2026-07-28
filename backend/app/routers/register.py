from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schema import RegisterUser, RegisterAdmin
from database.database import get_db
from app.model import User
from app.auth import hash_password

router = APIRouter()

@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):

    new_user = User(

        full_name=user.full_name,

        email=user.email,

        password=user.password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {"message":"Registered Successfully"}