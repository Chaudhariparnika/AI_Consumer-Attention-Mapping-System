from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from app.model import User, Admin
from app.schema import LoginUser, LoginAdmin
from app.auth import verify_password, create_access_token

router = APIRouter(
    prefix="/api",
    tags=["Login"]
)

# ---------------- USER LOGIN ---------------- #

@router.post("/user/login")
def login_user(
    user: LoginUser,
    db: Session = Depends(get_db)
):

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

    access_token = create_access_token(
        data={
            "id": db_user.id,
            "email": db_user.email,
            "role": "user"
        }
    )

    return {
        "message": "User Login Successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# ---------------- ADMIN LOGIN ---------------- #

@router.post("/admin/login")
def login_admin(
    admin: LoginAdmin,
    db: Session = Depends(get_db)
):

    db_admin = db.query(Admin).filter(
        Admin.email == admin.email
    ).first()

    if not db_admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        admin.password,
        db_admin.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        data={
            "id": db_admin.id,
            "email": db_admin.email,
            "role": "admin"
        }
    )

    return {
        "message": "Admin Login Successful",
        "access_token": access_token,
        "token_type": "bearer"
    }