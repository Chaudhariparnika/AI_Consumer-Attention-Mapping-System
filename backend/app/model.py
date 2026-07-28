import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))
from database.database import Base
from sqlalchemy import TIMESTAMP, VARCHAR, Column, Integer, String, Date, func

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)

  full_name = Column(VARCHAR(100), nullable=False)

  email = Column(VARCHAR(100), unique=True, nullable=False)
  
  phone_no = Column(Integer, unique=True, nullable=False)

  password = Column(VARCHAR(255), unique=True, nullable=False)

  role = Column(VARCHAR(20), nullable=True)

  created_at = Column(TIMESTAMP, default=func.current_timestamp())

class Admin(Base):
  __tablename__ = "admin"

  id = Column(Integer, primary_key=True, index=True)

  full_name = Column(VARCHAR(100), nullable=False)

  email = Column(VARCHAR(100), unique=True, nullable=False)
  
  phone_no = Column(Integer, unique=True, nullable=False)

  password = Column(VARCHAR(255), unique=True, nullable=False)

  role = Column(VARCHAR(20), nullable=True)

  created_at = Column(TIMESTAMP, default=func.current_timestamp())
