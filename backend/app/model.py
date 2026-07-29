import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone_no = Column(String(15), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False, default="user")

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone_no = Column(String(15), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False, default="admin")

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )