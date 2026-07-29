from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from app.schema import RegisterUser, UserResponse , RegisterAdmin, AdminResponse
from app.model import User, Admin
from app.auth import hash_password

router = APIRouter(
    prefix="/api",
    tags=["Register"]
)

#user registration endpoint
@router.post("/user/register", response_model=UserResponse)
def register_user(user: RegisterUser, db: Session = Depends(get_db)):

    # Check whether email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create User object
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_no=user.phone_no,
        password=hashed_password,
        role=user.role
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#Admin registration endpoint
@router.post("/admin/register", response_model=AdminResponse)
def register_admin(admin: RegisterAdmin, db: Session = Depends(get_db)):

    # Check whether email already exists
    existing_admin = db.query(Admin).filter(
        Admin.email == admin.email
    ).first()

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(admin.password)

    # Create Admin object
    new_admin = Admin(
        full_name=admin.full_name,
        email=admin.email,
        phone_no=admin.phone_no,
        password=hashed_password,
        role=admin.role
    )

    # Save to database
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin