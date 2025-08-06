from fastapi import FastAPI, Request
from send import send_message, hi_intro_message ,email_confirmation_message ,transport_mode_message
from config import PEPIPOST_API_KEY, PEPIPOST_BASE_URL, PEPIPOST_SOURCE
from state import upsert_user_state, get_user_state, clear_state
import asyncio
from data_extraction import incoming_data_extraction
from data_inputing import log_incoming_data, incoming_data_inputting_db
from database import Base, engine, SessionLocal
from models import WhatsAppMessage, User, IncomingMessage

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)
    message_info= incoming_data_extraction(data)
    incoming_data_inputting_db(message_info)
    
    
    user_number = message_info['from_number']
    if not message_info.get("from_number"):
        return {"error": "Invalid message structure — no sender phone number"}
    user_message = message_info['text'].strip()
    print(user_message)


    print(f"Message from {user_number}: {user_message}")
    log_incoming_data(message_received=user_message,recipient_number=user_number)

    db= SessionLocal()
    try: 
        user = db.query(User).filter_by(phone_number=user_number).first()

        if user is None:
            user = User(phone_number=user_number, user_state="new")
            db.add(user)
            db.commit()
  
        current_state= user.user_state

        if current_state in (None, "new"):
            if user_message.lower() in ["hi","hello"]:
                await hi_intro_message(user_number, "Hi ,   Welcome to the TRIP JACK!!")
                await send_message(user_number, "What is your name?")
                user.user_state="waiting_for_name"
                db.commit()
                return {"status": "asked_name"}
            else:
                await send_message(user_number, 'Please type "hi" or "Hello" to start the convocation')
                return {"status": "invalid_start"}

        elif current_state == "waiting_for_name":
            if any(char.isdigit() for char in user_message):
                await send_message(user_number,"Invalidname. Names can not contain digits ")
                return {"status": "invalid_name"}
            
            user.name=user_message
            await send_message(user_number, f"Nice to meet you, {user_message}")
            user.user_state= "waiting_for_email"
            db.commit()
            await send_message(user_number, f"{user_message}, Please share your email which you want to use to book the trips.")
            return {"status": "name_saved"}
        
        elif current_state == "waiting_for_email":
            user.email = user_message
            user.user_state = "awaiting_email_confirmation"
            db.commit()
            await send_message(user_number, f"Thank you for sharing your email: {user_message}.")
            await email_confirmation_message(user_number, "Please confirm you want to use this email to book your trips. (Yes/No)")
            return {"status": "awaiting_email_confirmation"}

        elif current_state == "awaiting_email_confirmation":
            if user_message.lower() == "yes":
                await send_message(user_number, "New email has been saved successfully and lets move ahead with the booking. Finished!!!")
                user.user_state= "select_mode_of_transport"
                await transport_mode_message(user_number, "Select the mode of transport")
                db.commit()
                return {"status": "new_email_recieved and moved to select transport"}        
            elif user_message.lower() == "no":
                user.user_state="waiting_for_email"
                await send_message(user_number, "Okay, Send your email again.")
                db.commit()
                return {"status":"invalid_email"}
            else:
                print(user_message)
                await send_message(user_number,"Please reply with yes or no")
                return {"status": "invalid_reply"}

        elif current_state == "select_mode_of_transport":
            user.user_state= "Completed"
            db.commit()
            return {"status": "Selected mode of transport"}
        
        else:
            user.user_state = None
            db.commit()
            await send_message(user_number, "Something went wrong. Lets start the converstaion again.")
            return {"status" : "reset"}


        
    except Exception as e:
        print(f"Error: {e}")
        user = db.query(User).filter_by(phone_number=user_number).first()
        if user:
            user.user_state = "new"
            user.name = None
            user.email = None
            db.commit()
        await send_message(user_number, "Something went wrong")
        return {"message":"something went wrong"}

    finally:
        db.close()

    return {"status": "Success"}