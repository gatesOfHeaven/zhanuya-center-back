from fastapi import status, HTTPException
from sqlalchemy import select, exists, func, or_, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import time, datetime, timedelta

from core.bases import BaseQuery
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
from .values import TIMEDELTA_BEFORE_START_TO_CONFIRM, TIMEDELTA_AFTER_START_TO_CONFIRM, TimeStatus


class Query(BaseQuery):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.select_with_relations = select(Slot).options(
            joinedload(Slot.workday).joinedload(Workday.doctor).options(
                joinedload(Doctor.profile),
                joinedload(Doctor.category),
                joinedload(Doctor.office).joinedload(Room.building),
                joinedload(Doctor.price_list).joinedload(Price.appointment_type)
            ),
            (joinedload(Slot.payment).options(
                joinedload(Payment.manager)
                .joinedload(Manager.profile)
            )),
            joinedload(Slot.payment).joinedload(Payment.terminal),
            joinedload(Slot.patient),
            joinedload(Slot.type),
            joinedload(Slot.records)
        )


    async def get(self, id: int, me: User | Terminal) -> Slot:
        query = self.select_with_relations.where(Slot.id == id)
        slot = await self.first(query)
        if slot is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Appointment Not Found'
            )
        Validator.validate_access(slot, me)
        return slot


    async def new(
        self,
        patient: User,
        workday: Workday,
        price: Price,
        starts_at: time,
        ends_at: time,
        as_patient: bool = True,
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
        await self.verify_is_patient_free(slot, patient, as_patient)

        query = select(func.max(Slot.index)).where(Slot.patient == patient)
        index = await self.field(query)
        slot.index = 1 if index is None else index + 1

        self.db.add(slot)
        if commit: await self.commit()
        return slot


    async def paginate_my(self, time_status: TimeStatus | None, offset: int, limit: int, patient: User) -> list[Slot]:
        query = self.select_with_relations.where(Slot.patient == patient).offset(offset).limit(limit)
        now = datetime.now()
        if time_status == TimeStatus.PAST: query = query.where(or_(
            Slot.date < now.date(),
            and_(
                Slot.date == now.date(),
                Slot.ends_at <= now.time()
            )
        )).order_by(Slot.date.desc(), Slot.starts_at.desc())
        elif time_status == TimeStatus.UPCOMING: query = query.where(or_(
            Slot.date > now.date(),
            and_(
                Slot.date == now.date(),
                Slot.ends_at > now.time()
            )
        )).order_by(Slot.date.asc(), Slot.starts_at.asc())
        else: query = query.order_by(Slot.date.desc(), Slot.starts_at.desc())
        return await self.fetch_all(query)


    async def total(self, patient: User, time_status: TimeStatus | None) -> int:
        query = select(func.count(Slot.id)).where(Slot.patient == patient)
        now = datetime.now()
        if time_status == TimeStatus.PAST: query = query.where(or_(
            Slot.date < now.date(),
            and_(
                Slot.date == now.date(),
                Slot.ends_at <= now.time()
            )
        ))
        elif time_status == TimeStatus.UPCOMING: query = query.where(or_(
            Slot.date > now.date(),
            and_(
                Slot.date == now.date(),
                Slot.ends_at > now.time()
            )
        ))
        return await self.field(query)


    async def upcomings(self) -> list[Slot]:
        after_halfhour = datetime.now() + timedelta(minutes = 30)
        query = self.select_with_relations.where(or_(
            Slot.date > after_halfhour.date(),
            and_(
                Slot.date == after_halfhour.date(),
                Slot.starts_at >= after_halfhour.time()
            )
        ))
        return await self.fetch_all(query)


    async def to_confirm(self, terminal: Terminal) -> list[Slot]:
        now = datetime.now()
        query = self.select_with_relations.where(
            Room.building_id == terminal.building_id,
            Slot.payment == None,
            Slot.date == now.date(),
            Slot.starts_at > (now - TIMEDELTA_BEFORE_START_TO_CONFIRM).time(),
            Slot.starts_at < (now + TIMEDELTA_AFTER_START_TO_CONFIRM).time()
        ).join(Slot.workday).join(Workday.doctor).join(Doctor.office)
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
        Validator.validate_patient(slot, me, 'Edit')
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
        await self.verify_is_patient_free(slot, me)
        
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


    async def verify_is_patient_free(self, slot: Slot, me: User, as_patient: bool = True) -> None:
        query = select(exists(Slot).where(
            Slot.date == slot.workday.date,
            Slot.starts_at < slot.ends_at,
            Slot.ends_at > slot.starts_at,
            Slot.patient_id == me.id,
            Slot.id != slot.id
        ))
        is_patient_busy = await self.field(query)
        who_have = 'You have' if as_patient else f'{me.fullname()} has'
        if is_patient_busy: raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE,
            f'{who_have} Another Appointment At This Time'
        )