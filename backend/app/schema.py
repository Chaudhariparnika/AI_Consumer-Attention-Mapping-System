from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.model import UserRole

# Register
class RegisterUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole

# Login
class LoginUser(BaseModel):
    email: EmailStr
    password: str

# Response
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str
    role: UserRole

# Store
class StoreBase(BaseModel):
    name: str
    location: str

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Camera
class CameraBase(BaseModel):
    name: str
    rtsp_url: str
    is_online: bool = True
    store_id: int

class CameraCreate(CameraBase):
    pass

class CameraResponse(CameraBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Dashboard
class OverviewMetrics(BaseModel):
    total_stores: int
    total_users: int
    total_cameras: int
    total_products: int
    total_shelves: int
    todays_visitors: int
    avg_dwell_time_mins: float
    active_ai_cameras: int
    product_engagement_score: float