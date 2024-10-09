from os import getenv


SERVER = getenv('SMTP_SERVER')
PORT = getenv('SMTP_PORT')
SENDER_EMAIL = getenv('SMTP_SENDER_EMAIL')
PASSWORD = getenv('SMTP_PASSWORD')