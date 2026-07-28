from database.database import SessionLocal
from app.auth import decode_access_token
#stop session
def get_db():  
  db = SessionLocal()
  try:
    yield db  
  finally:
    db.close()
    
  def get_current_user():
    pass  
  def get_current_admin():
    pass