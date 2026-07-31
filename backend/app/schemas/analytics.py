from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class DetectionCreate(BaseModel):
    camera_id: int
    store_id: int
    shelf_id: Optional[int] = None
    detected_class: str
    confidence: float
    bbox_x: int
    bbox_y: int
    bbox_w: int
    bbox_h: int


class DetectionResponse(DetectionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalyticsSummary(BaseModel):
    total_detections: int
    recent_classes: List[str]
