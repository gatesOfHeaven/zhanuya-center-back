from fastapi import HTTPException, status
from aiosmtplib import SMTP, SMTPException
from email.mime.text import MIMEText

from config import smtp


FROM_KEY = 'From'
TO_KEY = 'To'
SUBJECT_KEY = 'Subject'


async def send(
    reciever_email: str,
    subject: str,
    content: str
):
    message = MIMEText(content)
    message[FROM_KEY] = smtp.SENDER_EMAIL
    message[TO_KEY] = reciever_email
    message[SUBJECT_KEY] = f'Happy Patient - {subject}'
    server = SMTP(
        hostname = smtp.SERVER,
        port = smtp.PORT,
        username = smtp.SENDER_EMAIL,
        password = smtp.PASSWORD,
        use_tls = False
    )
    try:
        await server.connect()
        await server.send_message(message)
    except SMTPException as e:
        print(f'SMTP error: {e}')
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)