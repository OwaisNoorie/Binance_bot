# src/config.py
import os
from dotenv import load_dotenv

# Project root (one level above src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

# Load .env file
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TESTNET = os.getenv("TESTNET", "True").lower() in ("1", "true", "yes")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# Log file path
LOG_FILE = os.path.join(PROJECT_ROOT, "bot.log")
