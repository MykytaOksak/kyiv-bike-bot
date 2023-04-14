from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
ADMIN_ID = os.getenv('ADMIN_ID')
DIRECTIONS_API_ENDPOINT = os.getenv('DIRECTIONS_API_ENDPOINT')
STATIC_MAPS_API_ENDPOINT = os.getenv('STATIC_MAPS_API_ENDPOINT')
API_KEY = os.getenv('API_KEY')
URL_APP = os.getenv('URL')
APP_HOST = os.getenv('APP_HOST')
DATABASE_URL = os.getenv('DATABASE_URL')