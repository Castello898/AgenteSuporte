import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis do .env

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SHIPPING_API_URL = os.getenv("SHIPPING_API_URL")
SHIPPING_API_KEY = os.getenv("SHIPPING_API_KEY")
CRM_API_URL = os.getenv("CRM_API_URL")
CRM_API_KEY = os.getenv("CRM_API_KEY")