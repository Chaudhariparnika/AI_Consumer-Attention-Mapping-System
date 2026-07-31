from app.model import Store, Camera
from database.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)


def seed_cameras():
    db = SessionLocal()
    try:
        existing_store = db.query(Store).first()
        if not existing_store:
            store = Store(
                store_name="Demo Store",
                location="Downtown",
                manager_name="John Doe",
                total_shelves=10,
                total_cameras=10,
            )
            db.add(store)
            db.commit()
            db.refresh(store)
            existing_store = store

        existing_count = db.query(Camera).count()
        if existing_count >= 10:
            print(f"Camera seed already exists ({existing_count} cameras found).")
            return

        sample_cameras = []
        for i in range(1, 11):
            sample_cameras.append(
                Camera(
                    camera_name=f"Camera {i}",
                    store_id=existing_store.id,
                    rtsp_url=f"rtsp://demo-camera-{i}:554/stream",
                    location=f"Zone {i}",
                    status="Online",
                )
            )

        db.add_all(sample_cameras)
        db.commit()
        print("Inserted 10 sample cameras successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_cameras()
