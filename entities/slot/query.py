from fastapi import status, HTTPException
from sqlalchemy import select, exists, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import time

from utils.bases import BaseQuery
from entities.user import User
from entities.doctor import Doctor
from entities.manager import Manager
from entities.terminal import Terminal
from entities.workday import Workday
from entities.price import Price
from entities.room import Room
from entities.payment import Payment
from .entity import Slot
from .validator import Validator


class Query(BaseQuery):
    def __init__(self, db: AsyncSession):
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
            (joinedload(Slot.workday)
                .joinedload(Workday.doctor)
                .joinedload(Doctor.price_list)
                .joinedload(Price.appointment_type)
            ),
            joinedload(Slot.patient),
            joinedload(Slot.type),
            joinedload(Slot.payment).joinedload(Payment.terminal),
            (joinedload(Slot.payment)
                .joinedload(Payment.manager)
                .joinedload(Manager.profile)
            )
        )


    async def get(self, id: int, me: User | Terminal) -> Slot:
        query = self.select_with_relations.where(Slot.id == id)
        slot = await self.first(query)
        if slot is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Appointment Not Found'
            )
        
        doctor = slot.workday.doctor
        building = doctor.office.building
        im_patient = isinstance(me, User) and slot.patient == me
        im_doctor = isinstance(me, User) and doctor == me.as_doctor
        im_manager = isinstance(me, User) and isinstance(me.as_manager, Manager) and building == me.as_manager.building
        is_terminal = isinstance(me, Terminal) and building == me.building
        if not (im_patient or im_doctor or im_manager or is_terminal):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                'You Can See Only YOUR Appointments'
            )
        return slot


    async def new(
        self,
        patient: User,
        workday: Workday,
        price: Price,
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
            type = price.appointment_type,
            starts_at = starts_at,
            ends_at = ends_at,
            price = price.cost
        )
        Validator.validate_duration(slot, price.appointment_type)
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
        return await self.fetch_all(query)
        

    async def edit(
        self,
        slot: Slot,
        workday: Workday,
        price: Price,
        start_time: time,
        end_time: time,
        me: User,
        commit: bool = True
    ) -> Slot:
        Validator.validate_doesnt_start(slot, 'Edit')
        slot.workday = workday
        slot.type = price.appointment_type
        slot.starts_at = start_time
        slot.ends_at = end_time
        slot.price = price.cost

        Validator.validate_duration(slot, price.appointment_type)
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
            Slot.patient_id == me.id,
            Slot.id != slot.id
        ))
        am_i_busy = await self.field(query)
        if am_i_busy:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                'You Have Another Appointment At This Time'
            )