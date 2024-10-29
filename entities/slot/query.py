from fastapi import status, HTTPException
from sqlalchemy import select, exists, func
from sqlalchemy.orm import joinedload
from datetime import datetime, time, timedelta

from utils.bases import BaseQuery
from entities.user import User
from entities.doctor import Doctor
from entities.workday import Workday
from entities.appointment_type import AppointmentType
from entities.room import Room
from .entity import Slot
from .validator import Validator


class Query(BaseQuery):
    def __init__(self, db):
        super().__init__(db)
        self.select_with_relations = select(Slot).options(
            (joinedload(Slot.workday)
                .joinedload(Workday.doctor)
                .joinedload(Doctor.profile)
            ),
            (joinedload(Slot.workday)
                .joinedload(Workday.doctor)
                .joinedload(Doctor.category)
            ),
            (joinedload(Slot.workday)
                .joinedload(Workday.doctor)
                .joinedload(Doctor.office)
                .joinedload(Room.building)
            ),
            joinedload(Slot.patient),
            joinedload(Slot.type)
        )


    async def get(self, id: int, me: User) -> Slot:
        query = self.select_with_relations.where(Slot.id == id)
        slot = await self.first(query)
        if slot is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Appointment Not Found'
            )
        Validator.validate_patient(slot, me, 'See')
        return slot


    async def new(
        self,
        patient: User,
        workday: Workday,
        appointment_type: AppointmentType,
        starts_at: time,
        ends_at: time,
        commit: bool = True
    ) -> Slot:
        if patient.id == workday.doctor_id:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                'You Cannot Make Appointment For Yourself'
            )
        
        slot = Slot(
            patient = patient,
            workday = workday,
            type = appointment_type,
            starts_at = starts_at,
            ends_at = ends_at
        )
        Validator.validate_duration(slot, appointment_type)
        Validator.validate_workday_time(slot)
        await self.verify_occupation(slot)
        Validator.validate_isnt_past(slot)
        await self.verify_am_i_free(slot, patient)

        query = select(func.max(Slot.index)).where(Slot.patient == patient)
        index = await self.field(query)
        slot.index = 1 if index is None else index + 1

        self.db.add(slot)
        if commit: await self.commit()
        return slot
    

    async def my(self, me: User) -> list[Slot]:
        query = self.select_with_relations.where(Slot.patient_id == me.id)
        return await self.all(query)
    

    async def upcomings(self) -> list[Slot]:
        query = self.select_with_relations.where(
            datetime.combine(Slot.date, Slot.starts_at) - datetime.now() <= timedelta(minutes = 30)
        )
        return await self.all(query)
        

    async def edit(
        self,
        slot: Slot,
        workday: Workday,
        appointment_type: AppointmentType,
        start_time: time,
        end_time: time,
        me: User,
        commit: bool = True
    ) -> Slot:
        Validator.validate_doesnt_start(slot, 'Edit')
        slot.workday = workday
        slot.type = appointment_type
        slot.starts_at = start_time
        slot.ends_at = end_time
        Validator.validate_duration(slot, appointment_type)
        Validator.validate_workday_time(slot)
        await self.verify_occupation(slot)
        Validator.validate_isnt_past(slot)
        await self.verify_am_i_free(slot, me)
        
        if commit: await self.commit()
        return slot


    async def remove(self, slot: Slot, me: User, commit: bool = True) -> None:
        Validator.validate_patient(slot, me, 'Cancel')
        Validator.validate_doesnt_start(slot, 'Cancel')
        await self.db.delete(slot)
        if commit: await self.commit()


    async def verify_occupation(self, slot: Slot) -> None:
        query = select(exists(Slot).where(
            Slot.date == slot.workday.date,
            Slot.doctor_id == slot.workday.doctor_id,
            Slot.starts_at < slot.ends_at,
            Slot.ends_at > slot.starts_at,
            Slot.id != slot.id
        ))
        slot_is_busy = await self.field(query)
        if slot_is_busy:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                'Such Doctor For Such Time Unavailable'
            )


    async def verify_am_i_free(self, slot: Slot, me: User) -> None:
        query = select(exists(Slot).where(
            Slot.date == slot.workday.date,
            Slot.starts_at < slot.ends_at,
            Slot.ends_at > slot.starts_at,
            Slot.patient_id == me.id
        ))
        am_i_busy = await self.field(query)
        if am_i_busy:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                'You Have Another Appointment At This Time'
            )