from dotenv import load_dotenv
import os

load_dotenv()  

PEPIPOST_API_KEY = os.getenv("PEPIPOST_API_KEY")
PEPIPOST_BASE_URL = os.getenv("PEPIPOST_BASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
PEPIPOST_SOURCE = os.getenv("PEPIPOST_SOURCE")