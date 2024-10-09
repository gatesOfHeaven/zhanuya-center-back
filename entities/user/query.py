from fastapi import HTTPException, status
from sqlalchemy import select, exists
from sqlalchemy.orm import joinedload
from datetime import date

from utils.bases import BaseQuery
from utils.facades import calc
from entities.role import RoleID
from .entity import User


class Query(BaseQuery):
    async def new(
        self,
        email: str,
        iin: str,
        name: str,
        surname: str,
        gender: str,
        birth_date: str,
        password_hash: str,
        commit: bool = True
    ) -> User:
        query = select(exists(User).where(User.email == email))
        email_used = (await self.db.execute(query)).scalar()
        if email_used:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                'This Email Already Taken'
            )

        birth_date: date = calc.str_to_time(birth_date, '%d-%m-%Y').date()
        user = User(
            role_id = RoleID.PATIENT.value,
            email = email,
            iin = iin,
            name = name,
            surname = surname,
            gender = gender,
            birth_date = birth_date,
            password_hash = password_hash
        )
        self.db.add(user)

        if commit: await self.commit()
        return user
        

    async def get_by_email(self, email: str, password_hash: str) -> User:
        query = select(User).where(
            User.email == email,
            User.password_hash == password_hash
        ).options(joinedload(User.role))
        user = (await self.db.execute(query)).scalar_one_or_none()

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'User[email={email} & password] Not Found'
            )
        return user
        

    async def get_by_iin(self, iin: str, password_hash: str) -> User:
        query = select(User).where(
            User.iin == iin,
            User.password_hash == password_hash
        ).options(joinedload(User.role))
        user = (await self.db.execute(query)).scalar_one_or_none()

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'User[iin={iin} & password] Not Found'
            )
        return user
    
    
    async def get_by_id(self, id: int) -> User:
        query = select(User).where(User.id == id).options(
            joinedload(User.role)
        )
        user = (await self.db.execute(query)).scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'User[id={id}] Not Found'
            )
        return user