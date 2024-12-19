from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from datetime import datetime

from core.bases import BaseQuery
from entities.user import User
from entities.slot import Slot
from entities.workday import Workday
from entities.doctor import Doctor
from entities.room import Room
from .entity import MedicalRecord
from .values import MedicalRecordType


class Query(BaseQuery):
    async def new(self, slot: Slot, record_type: MedicalRecordType, title: str, content: str) -> MedicalRecord:
        medical_record = MedicalRecord(
            slot = slot,
            type = record_type,
            added_at = datetime.now(),
            title = title,
            content = content
        )
        self.db.add(medical_record)
        await self.commit()
        return medical_record
    

    async def get(self, id: int, me: User) -> MedicalRecord:
        query = select(MedicalRecord).options(
            joinedload(MedicalRecord.slot).options(
                joinedload(Slot.patient),
                joinedload(Slot.workday).joinedload(Workday.doctor).options(
                    joinedload(Doctor.office).joinedload(Room.building),
                    joinedload(Doctor.profile)
                )
            )
        ).where(MedicalRecord.id == id, Doctor.profile == me)

        medical_record = await self.first(query)
        if medical_record is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Medical Record Not Found'
            )
        return medical_record


    async def edit(
        self,
        medical_record: MedicalRecord,
        record_type: MedicalRecordType | None,
        title: str | None,
        content: str | None
    ) -> MedicalRecord:
        if record_type is not None: medical_record.type = record_type
        if title is not None: medical_record.type = title
        if content is not None: medical_record.type = content

        await self.commit()
        return medical_record


    async def delete(self, medical_record: MedicalRecord):
        await self.db.delete(medical_record)
        await self.commit()


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