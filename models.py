from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, func
from datetime import datetime
from database import Base

class WhatsAppMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    direction = Column(String, index=True)
    sender = Column(String)
    recipient = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    phone_number = Column(String, primary_key=True)  # Still declared as primary key
    name = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_state = Column(String, nullable=True)
    email = Column(String, nullable=True)

class IncomingMessage(Base):
    __tablename__ = "incoming_data_info"

    id = Column(Integer, primary_key=True, index=True)
    context_message_id = Column(Text,nullable=True)
    context_ncmessage_id = Column(Text,nullable=True)
    from_number = Column(String(20))
    from_name = Column(String(100))
    message_id = Column(Text)
    message_type = Column(String(20))
    received_at = Column(BigInteger,nullable=True)
    text = Column(Text)
    to_number = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())