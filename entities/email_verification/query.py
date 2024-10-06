from fastapi import HTTPException, status
from sqlalchemy import select
from datetime import datetime, timedelta

from utils.bases import BaseQuery
from .entity import EmailVerification


class Query(BaseQuery):
    async def get(self, email: str) -> EmailVerification | None:
        query = select(EmailVerification).where(EmailVerification.email == email)
        verification_record = (await self.db.execute(query)).scalar_one_or_none()
        if verification_record is None: return None

        expired: bool = verification_record.expires_at < datetime.now()
        verified: bool = verification_record.verified_at is not None

        if expired and not verified:
            await self.db.delete(verification_record)
            await self.commit()
            return None
        return verification_record


    async def new(
        self,
        email: str,
        verification_code: int,
        commit: bool = True
    ) -> EmailVerification:
        verification_record = await self.get(email)
        if verification_record is not None:
            if verification_record.verified_at is not None:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    'This Email Already Taken'
                )
            verification_record.code = verification_code
        else:
            expires_at = datetime.now() + timedelta(minutes = 15)
            verification_record = EmailVerification(
                email = email,
                code = verification_code,
                expires_at = expires_at
            )
            self.db.add(verification_record)

        if commit: await self.commit()
        return verification_record
    

    async def verify(
        self,
        email: str,
        verification_code: int,
        commit: bool = True
    ) -> EmailVerification:
        verification_record = await self.get(email)
        if verification_record is None:
            raise HTTPException(
                status.HTTP_408_REQUEST_TIMEOUT,
                'There is no valid Verification Code. Please, try again'
            )        
        if verification_record.code != verification_code:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Wrong Code. Please, try again'
            )
        
        verification_record.verified_at = datetime.now()
        if commit: await self.commit()
        return verification_record
