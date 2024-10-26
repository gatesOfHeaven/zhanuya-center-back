from fastapi import HTTPException, status
from sqlalchemy import select, exists, or_, func
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
        password: str, # test only
        password_hash: str,
        commit: bool = True
    ) -> User:
        query = select(exists(User).where(
            or_(User.email == email, User.iin == iin)
        ))
        credentials_used = await self.field(query)
        if credentials_used:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                'This Credentials Already Taken'
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
            password = password, # test only
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


    async def iin_is_available(self, iin: str) -> bool:
        query = select(exists(User).where(User.iin == iin))
        return not await self.field(query)


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
    

    async def get_random(self, count: int) -> list[User]:
        query = select(User).options(
            joinedload(User.role)
        ).order_by(func.random()).limit(count)
        return (await self.db.execute(query)).scalars().all()