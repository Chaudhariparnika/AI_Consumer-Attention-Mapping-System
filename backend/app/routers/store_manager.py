from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from app.dependencies import require_admin
from app import model, schema

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/overview", response_model=schema.OverviewMetrics)
def get_dashboard_overview(
    db: Session = Depends(get_db),
    admin_user: model.User = Depends(require_admin)
):
    total_stores = db.query(model.Store).count()
    total_users = db.query(model.User).count()
    total_cameras = db.query(model.Camera).count()
    active_cameras = db.query(model.Camera).filter(model.Camera.is_online == True).count()
    total_products = db.query(model.Product).count()
    total_shelves = db.query(model.Shelf).count()

    return schema.OverviewMetrics(
        total_stores=total_stores,
        total_users=total_users,
        total_cameras=total_cameras,
        total_products=total_products,
        total_shelves=total_shelves,
        todays_visitors=2840,
        avg_dwell_time_mins=6.4,
        active_ai_cameras=active_cameras,
        product_engagement_score=87.5
    )