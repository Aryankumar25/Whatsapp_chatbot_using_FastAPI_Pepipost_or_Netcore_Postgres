# user_state ={}

# def set_state(phone_number: str, state: str):
#     user_state[phone_number] = state

# def get_state(phone_number:str) -> str:
#     return user_state.get(phone_number)

# def clear_state(phone_number: str):
#     if phone_number in user_state:
#         del user_state[phone_number]

from sqlalchemy.orm import Session
from models import User   # Assuming your model is named UserState
from database import SessionLocal  # Your session

def upsert_user_state(phone_number: str, new_state: str):
    db: Session = SessionLocal()
    try:
        user = db.query(UserState).filter_by(phone_number=phone_number).first()
        if user:
            user.user_state = new_state
        else:
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

def clear_state(phone_number: str, new_state: str):
    db: Session = SessionLocal()
    try:
        user = db.query(UserState).filter_by(phone_number=phone_number).first()
        if phone_number in user.user_state:
            user.user_state=new_state
            db.add(user)

        db.commit()
    finally:
        db.close()

            