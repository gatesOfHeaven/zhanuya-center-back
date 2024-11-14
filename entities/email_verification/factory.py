from random import randint
from datetime import date, timedelta

from utils.bases import BaseFactory
from entities.user import User, Role
from .entity import EmailVerification
from .values import code_expiring_mins


class Factory(BaseFactory):
    async def seed(self, users: list[User]):
        fakes: list[EmailVerification] = []

        for user in users:
            if user.role_type == Role.PATIENT:
                expires_at = self.fake.date_time_between(
                    start_date = user.birth_date,
                    end_date = date.today()
                )
                verified_at = self.fake.date_time_between(
                    start_date = expires_at - timedelta(minutes = code_expiring_mins),
                    end_date = expires_at
                )
                email_verification = EmailVerification(
                    email = user.email,
                    code = randint(1000, 9999),
                    expires_at = expires_at,
                    verified_at = verified_at
                )
            else:
                email_verification = EmailVerification(
                    email = self.fake.email(),
                    code = randint(1000, 9999),
                    expires_at = self.fake.date_time()
                )
            fakes.append(email_verification)
        await self.flush(fakes)
        return fakes