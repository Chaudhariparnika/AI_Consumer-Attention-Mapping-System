from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from app import model
from app.schemas.analytics import AnalyticsSummary, DetectionCreate, DetectionResponse
from app.services.yolo_service import YOLOService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
yolo_service = YOLOService()


@router.post("/detect", response_model=DetectionResponse, status_code=status.HTTP_201_CREATED)
def save_detection(payload: DetectionCreate, db: Session = Depends(get_db)):
    camera = db.query(model.Camera).filter(model.Camera.id == payload.camera_id).first()
    store = db.query(model.Store).filter(model.Store.id == payload.store_id).first()

    if not camera or not store:
        raise HTTPException(status_code=404, detail="Camera or store not found")

    detection = model.Detection(
        camera_id=payload.camera_id,
        store_id=payload.store_id,
        shelf_id=payload.shelf_id,
        detected_class=payload.detected_class,
        confidence=payload.confidence,
        bbox_x=payload.bbox_x,
        bbox_y=payload.bbox_y,
        bbox_w=payload.bbox_w,
        bbox_h=payload.bbox_h,
    )

    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection


@router.get("/recent", response_model=List[DetectionResponse])
def get_recent_detections(db: Session = Depends(get_db)):
    detections = db.query(model.Detection).order_by(model.Detection.created_at.desc()).limit(20).all()
    return detections


@router.get("/summary", response_model=AnalyticsSummary)
def get_summary(db: Session = Depends(get_db)):
    total_detections = db.query(model.Detection).count()
    recent_rows = db.query(model.Detection).order_by(model.Detection.created_at.desc()).limit(10).all()
    recent_classes = [row.detected_class for row in recent_rows]
    return AnalyticsSummary(total_detections=total_detections, recent_classes=recent_classes)


@router.post("/run", status_code=status.HTTP_200_OK)
def run_detection_for_camera(camera_id: int, db: Session = Depends(get_db)):
    camera = db.query(model.Camera).filter(model.Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    if not camera.rtsp_url:
        raise HTTPException(status_code=400, detail="Camera RTSP URL is missing")

    detections = yolo_service.process_rtsp_url(camera.rtsp_url)
    return {"camera_id": camera_id, "detections": detections}
