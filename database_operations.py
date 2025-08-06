from sqlalchemy.orm import Session
from models import UserState  # Assuming your model is named UserState
from database import SessionLocal  # Your session

def upsert_user_state(phone_number: str, new_state: str):
    db: Session = SessionLocal()
    try:
        user = db.query(UserState).filter_by(phone_number=phone_number).first()
        
        if user:
            # ✅ Update the existing user state directly
            user.user_state = new_state
        else:
            # ✅ Create new user state record
            user = UserState(phone_number=phone_number, user_state=new_state)
            db.add(user)

        db.commit()
    finally:
        db.close()

def get_user_state(phone_number: str):
    db: Session = SessionLocal()
    try:
        user = db.query(UserState).filter_by(phone_number=phone_number).first()
        return user.user_state if user else None
    finally:
        db.close()
