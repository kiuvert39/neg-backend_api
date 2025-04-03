import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    MONGO_URI = os.getenv("MONGO_URI")
    FREEIMAGE_HOST_API_URL = os.getenv("FREEIMAGE_HOST_API_URL")
    FREEIMAGE_HOST_API_KEY = os.getenv("FREEIMAGE_HOST_API_KEY")
    FRONTEND_URL = os.getenv("frontend_url")
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"] 


class DevConfig(Config):
    pass  # Inherits everything from Config

class ProdConfig(Config):
    DEBUG = False  # Explicitly set DEBUG to False in production