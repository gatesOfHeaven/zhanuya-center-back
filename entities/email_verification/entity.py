from sqlalchemy import Column, Integer, String, DateTime

from core.bases import BaseEntity


class EmailVerification(BaseEntity):
    __tablename__ = 'email_verifications'

    email = Column(String, primary_key = True)
    code = Column(Integer, nullable = False)
    expires_at = Column(DateTime, nullable = False)
    verified_at = Column(DateTime, nullable = True)