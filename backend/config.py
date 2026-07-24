import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'autoelite-dev-secret-key-change-in-prod')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/car_dealership')
    # Neon.tech requires SSL
    SSL_MODE = os.getenv('SSL_MODE', 'require')
