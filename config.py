import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

DEFAULT_COMMANDS = [
    ("start", "Начать сначала"),
]


# For amoCRM
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
SUBDOMAIN = os.environ.get('SUBDOMAIN')
REDIRECT_URL = os.environ.get('REDIRECT_URL')