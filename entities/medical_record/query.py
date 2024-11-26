from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from utils.bases import BaseQuery
from entities.user import User
from entities.slot import Slot
from entities.workday import Workday
from entities.doctor import Doctor
from .entity import MedicalRecord
from .values import MedicalRecordType


class Query(BaseQuery):
    async def total(self, patient: User, record_type: MedicalRecordType | None) -> int:
        query = select(func.count(MedicalRecord.id)).where(
            MedicalRecord.slot.has(Slot.patient == patient),
            MedicalRecord.type == record_type if record_type is not None else True
        )
        return await self.field(query)


    async def paginate(
        self,
        patient: User,
        record_type: MedicalRecordType | None,
        offset: int,
        limit: int
    ) -> list[MedicalRecord]:
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
            .where(
                MedicalRecord.slot.has(Slot.patient == patient),
                MedicalRecord.type == record_type if record_type is not None else True
            )
            .offset(offset).limit(limit)
        )
        return await self.fetch_all(query)