import sys
from pathlib import Path
import enum
from datetime import datetime
from sqlalchemy.orm import relationship
from database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Boolean, DateTime, ForeignKey, Float, Enum


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STORE_MANAGER = "store_manager"
    RETAIL_ANALYST = "retail_analyst"
    MARKETING_ANALYST = "marketing_analyst"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    role = Column(
    Enum(
        UserRole,
        values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False
    )
    password = Column(String(255), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    store = relationship("Store", back_populates="users")


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(100), nullable=False)
    location = Column(String(150))
    manager_name = Column(String(100))
    total_shelves = Column(Integer, default=0)
    total_cameras = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="store")
    shelves = relationship("Shelf", back_populates="store")
    cameras = relationship("Camera", back_populates="store")
    analytics = relationship("Analytics", back_populates="store")


class Shelf(Base):
    __tablename__ = "shelves"

    id = Column(Integer, primary_key=True, index=True)
    shelf_name = Column(String(100), nullable=False)
    shelf_number = Column(String(20), unique=True, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    category = Column(String(100))
    aisle = Column(String(50))
    capacity = Column(Integer, default=0)
    status = Column(String(20), default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    store = relationship("Store", back_populates="shelves")
    products = relationship("Product", back_populates="shelf")
    analytics = relationship("Analytics", back_populates="shelf")
   

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    shelf_id = Column(Integer, ForeignKey("shelves.id"), nullable=False)
    shelf = relationship("Shelf", back_populates="products")


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    camera_name = Column(String(100))
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    rtsp_url = Column(String)
    location = Column(String(100))
    status = Column(String(20), default="Online")
    installed_on = Column(DateTime(timezone=True), server_default=func.now())
    store = relationship("Store", back_populates="cameras")
    analytics = relationship("Analytics", back_populates="camera")
    
class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer)

    store_id = Column(Integer, ForeignKey("stores.id"))
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    shelf_id = Column(Integer, ForeignKey("shelves.id"))

    viewed_product = Column(String(100))
    dwell_time = Column(Float)
    attention_score = Column(Float)

    visit_time = Column(DateTime(timezone=True), server_default=func.now())

    store = relationship("Store", back_populates="analytics")
    camera = relationship("Camera", back_populates="analytics")
    shelf = relationship("Shelf", back_populates="analytics")


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    shelf_id = Column(Integer, ForeignKey("shelves.id"), nullable=True)
    detected_class = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    bbox_x = Column(Integer, nullable=False)
    bbox_y = Column(Integer, nullable=False)
    bbox_w = Column(Integer, nullable=False)
    bbox_h = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())