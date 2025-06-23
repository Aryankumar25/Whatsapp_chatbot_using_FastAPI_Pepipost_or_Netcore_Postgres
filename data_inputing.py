from config import PEPIPOST_API_KEY, PEPIPOST_BASE_URL, PEPIPOST_SOURCE
from database import Base, engine, SessionLocal
from models import WhatsAppMessage, User, IncomingMessage


def log_outgoing_data(recipient_whatsapp: str, content: str):
    db = SessionLocal()
    try:
        db.add(WhatsAppMessage(
            direction="outgoing",
            sender=PEPIPOST_SOURCE,
            recipient=recipient_whatsapp,
            message=content
        ))
        db.commit()
    finally:
        db.close()

def log_incoming_data(message_received:str,recipient_number: str):
    db = SessionLocal()
    try:
        db.add(WhatsAppMessage(
            direction="incoming",
            sender=PEPIPOST_SOURCE,
            recipient=recipient_number,
            message=message_received
        ))

        user=db.query(User).filter_by(phone_number=recipient_number).first()
        if not user:
            user=User(phone_number=recipient_number, user_state="new")
            db.add(user)
        db.commit()
    finally:
        db.close()

def incoming_data_inputting_db(message_info: dict | None):
    if not isinstance(message_info, dict):
        print("warning: message_info is not a valid dict")
        return

    db= SessionLocal()
    try:
        db.add(IncomingMessage(
            context_message_id = message_info.get('context_message_id'),
            context_ncmessage_id= message_info.get('context_ncmessage_id'),
            from_number= message_info['from_number'],
            from_name= message_info['from_name'],
            message_id= message_info['message_id'],
            message_type= message_info['message_type'],
            received_at=message_info['received_at'],
            text= message_info['text'] ,
            to_number =message_info['to_number'],
        ))
        db.commit()
    except Exception as e:
        db.rollback()
        print("DB error" , e)
    finally:
        db.close()