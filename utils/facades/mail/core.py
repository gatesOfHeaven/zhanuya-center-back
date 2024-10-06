from fastapi import HTTPException, status
from smtplib import SMTP

from config import smtp


def send_verification_code(reciever_email: str, code: int):
    with SMTP(smtp.SERVER, smtp.PORT) as server:
        server.starttls()
        server.login(smtp.SENDER_EMAIL, smtp.PASSWORD)
        server.sendmail(
            smtp.SENDER_EMAIL,
            reciever_email,
            f'Your verification code is {code}'
        )