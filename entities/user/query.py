from fastapi import HTTPException, status
from sqlalchemy import select, exists, or_
from sqlalchemy.orm import joinedload
from datetime import date

from utils.bases import BaseQuery
from entities.doctor import Doctor
from entities.manager import Manager
from entities.room import Room
from entities.price import Price
from .entity import User


class Query(BaseQuery):
    async def new(
        self,
        email: str,
        iin: str,
        name: str,
        surname: str,
        gender: str,
        birth_date: date,
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

        user = User(
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
        )
        user = await self.first(query)

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
        )
        user = await self.first(query)

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f'User[iin={iin} & password] Not Found'
            )
        return user
    
    
    async def get_by_id(self, id: int) -> User | None:
        query = select(User).options(
            joinedload(User.as_doctor).options(
                joinedload(Doctor.office).joinedload(Room.building),
                joinedload(Doctor.price_list).joinedload(Price.appointment_type),
                joinedload(Doctor.category)
            ),
            joinedload(User.as_manager).joinedload(Manager.building)
        ).where(User.id == id)
        return await self.first(query)