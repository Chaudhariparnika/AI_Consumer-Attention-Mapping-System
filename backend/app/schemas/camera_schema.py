from pydantic import BaseModel
from typing import Optional


class CameraCreate(BaseModel):
    camera_name: str
    store_id: int
    rtsp_url: str
    location: str
    status: Optional[str] = "Online"


class CameraUpdate(BaseModel):
    camera_name: Optional[str] = None
    store_id: Optional[int] = None
    rtsp_url: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


class CameraResponse(BaseModel):
    id: int
    camera_name: str
    store_id: int
    rtsp_url: str
    location: str
    status: str

    class Config:
        from_attributes = True