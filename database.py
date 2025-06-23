from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from sqlalchemy.orm import declarative_base

Base = declarative_base()


engine = create_engine(DATABASE_URL)

# SessionLocal is used to interact with the DB session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for defining models
Base = declarative_base()
