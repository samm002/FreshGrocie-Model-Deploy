# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    FATSECRET_CONSUMER_KEY = os.environ.get('FATSECRET_CONSUMER_KEY', '')
    FATSECRET_CONSUMER_SECRET = os.environ.get('FATSECRET_CONSUMER_SECRET', '')
    FATSECRET_BASE_URL = os.environ.get('FATSECRET_BASE_URL', '')
    MODEL_PATH = os.environ.get('MODEL_PATH', 'model_freshgrocie.h5')