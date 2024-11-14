from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from utils.bases import BaseQuery
from entities.user import User
from entities.slot import Slot
from entities.workday import Workday
from entities.doctor import Doctor
from .entity import MedicalRecord


class Query(BaseQuery):
    async def total(self, me: User) -> int:
        query = (
            select(func.count(MedicalRecord.id))
            .where(MedicalRecord.slot.has(Slot.patient == me))
        )
        return await self.field(query)


    async def paginate(self, me: User, offset: int, limit: int) -> list[MedicalRecord]:
        query = (
            select(MedicalRecord)
            .options(
                joinedload(MedicalRecord.slot).options(
                    joinedload(Slot.type),
                    joinedload(Slot.workday).joinedload(Workday.doctor).options(
                        joinedload(Doctor.profile),
                        joinedload(Doctor.category)
                    )
                )
            )
            .where(MedicalRecord.slot.has(Slot.patient == me))
            .offset(offset).limit(limit)
        )
        return await self.fetch_all(query)