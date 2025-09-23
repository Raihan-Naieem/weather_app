import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
