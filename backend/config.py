import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Fallback for security
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
