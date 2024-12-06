from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.bases import BaseQuery
from entities.doctor import Doctor
from entities.appointment_type import AppointmentType
from .entity import Price


class Query(BaseQuery):
    async def get(
        self,
        doctor: Doctor,
        appointment_type: AppointmentType
    ) -> Price:
        query = select(Price).where(
            Price.doctor == doctor,
            Price.appointment_type == appointment_type
        )
        price = await self.first(query)
        if price is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Doctor Has No Such Type of Appointments'
            )
        return price
    

    async def all(self, doctor: Doctor) -> list[Price]:
        query = select(Price).where(Price.doctor == doctor)
        await self.fetch_all(query)