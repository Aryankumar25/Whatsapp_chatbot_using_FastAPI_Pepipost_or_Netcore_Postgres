import httpx
from config import PEPIPOST_API_KEY, PEPIPOST_BASE_URL, PEPIPOST_SOURCE
from database import Base, engine, SessionLocal
from models import WhatsAppMessage
from data_inputing import log_outgoing_data

async def transport_mode_message(recipient_number:str , content: str):
    headers={
        "Authorization": f"Bearer {PEPIPOST_API_KEY}",
        "Content-Type": "application/json"
    }

    payload ={
        "message": [
            {
                "recipient_whatsapp": recipient_number,
                "message_type": "interactive",
                "recipient_type": "individual",

                "type_interactive": [
                    {
                        "type": "list",
                        "footer": "Please select one",
                        "body": content,
                        "action" : [
                            {
                                "button" : "Menu List",
                                "sections": [
                                    {
                                        "title": "Option 1",
                                        "rows":[
                                            {
                                                "id": "id1",
                                                "title": "FLIGHT",
                                            }
                                        ]
                                    },
                                    {
                                        "title": "Option 2",
                                        "rows":[
                                            {
                                                "id": "id1",
                                                "title": "TRAIN",
                                            }
                                        ]
                                    },
                                    {
                                        "title": "Option 3",
                                        "rows":[
                                            {
                                                "id": "id1",
                                                "title": "BUS",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    log_outgoing_data(recipient_whatsapp=recipient_number, content=content)
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(PEPIPOST_BASE_URL, json=payload, headers=headers)
        print(f"Pepipost response: {response.status_code} - {response.text}")

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(" Failed to send message:", response.text)

async def hi_intro_message(recipient_number: str,content:str):
    headers = {
        "Authorization": f"Bearer {PEPIPOST_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": [
            {
                "recipient_whatsapp": recipient_number,
                "recipient_type": "individual",
                "message_type": "media",
                "source": PEPIPOST_SOURCE,
                "type_media": [
                    {   
                        "attachments":[
                            {
                                "attachment_type": "image",
                                "attachment_url": "https://my-experiment-buckent.s3.ap-south-1.amazonaws.com/Screenshot+2025-06-17+154611.png",
                                "caption": content,
                                "attachment_id": "img001"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    log_outgoing_data(recipient_whatsapp=recipient_number, content=content)
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(PEPIPOST_BASE_URL, json=payload, headers=headers)
        print(f"Pepipost response: {response.status_code} - {response.text}")

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(" Failed to send message:", response.text)


async def email_confirmation_message(recipient_number:str, content:str):
    headers={
        "Authorization": f"Bearer {PEPIPOST_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message":[
            {
                "recipient_whatsapp": recipient_number,
                "message_type": "interactive",
                "recipient_type": "individual",
                "type_interactive": [
                    {
                        "type":"button",
                        "body": content,
                        "footer":"Please Confirm",
                        "action": [
                            {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "yes",
                                            "title": "Yes"
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "No",
                                            "title": "No"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    log_outgoing_data(recipient_whatsapp=recipient_number, content=content)

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(PEPIPOST_BASE_URL, json=payload, headers=headers)
        print(f"Pepipost response: {response.status_code} - {response.text}")

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(" Failed to send message:", response.text)



async def send_message(recipient_number: str, content: str):
    headers = {
        "Authorization": f"Bearer {PEPIPOST_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": [
            {
                "recipient_whatsapp": recipient_number,
                "recipient_type": "individual",
                "message_type": "Text",
                "type_text": [
                    {
                        "content": content
                    }
                ]
            }
        ]
    }
    log_outgoing_data(recipient_whatsapp=recipient_number, content=content)

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(PEPIPOST_BASE_URL, json=payload, headers=headers)
        print(f"Pepipost response: {response.status_code} - {response.text}")

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(" Failed to send message:", response.text)    