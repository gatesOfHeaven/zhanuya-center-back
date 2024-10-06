from os import getenv
from dotenv import load_dotenv


load_dotenv()


SERVER = getenv('SMTP_SERVER')
PORT = getenv('SMTP_PORT')
SENDER_EMAIL = getenv('SMTP_SENDER_EMAIL')
PASSWORD = getenv('SMTP_PASSWORD')