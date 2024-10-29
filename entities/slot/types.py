from pydantic import BaseModel, Field
from datetime import datetime

from utils.facades import calc
from entities.user import User, PatientAsForeign
from entities.doctor import DoctorAsForeign
from entities.role import RoleID
from entities.category import CategoryAsForeign
from entities.room import RoomAsPrimary
from entities.appointment_type import AppointmentTypeAsForeign
from .entity import Slot
    

class MakeAppointmentReq(BaseModel):
    doctorId: int = Field(gt = 0)
    date: str = Field(pattern = r'\d{2}\.\d{2}\.\d{4}')
    typeId: int = Field(gt = 0)
    startsAt: str = Field(pattern = r'\d{2}\:\d{2}\:\d{2}')
    endsAt: str = Field(pattern = r'\d{2}\:\d{2}\:\d{2}')


class SlotAsPrimary(BaseModel):
    id: int
    date: str
    index: int
    startTime: str
    endTime: str
    isFinished: bool
    type: AppointmentTypeAsForeign
    category: CategoryAsForeign
    room: RoomAsPrimary
    doctor: DoctorAsForeign
    patient: PatientAsForeign

    def to_json(slot: Slot):
        return SlotAsPrimary(
            id = slot.id,
            date = calc.time_to_str(slot.workday.date),
            index = slot.index,
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            isFinished = datetime.now() > datetime.combine(slot.date, slot.ends_at),
            type = AppointmentTypeAsForeign.to_json(slot.type),
            category = CategoryAsForeign.to_json(slot.workday.doctor.category),
            room = RoomAsPrimary.to_json(slot.workday.doctor.office),
            doctor = DoctorAsForeign.to_json(slot.workday.doctor),
            patient = PatientAsForeign.to_json(slot.patient)
        ).model_dump()


class SlotAsForeign(BaseModel):
    id: int
    startTime: str
    endTime: str
    mine: bool

    def to_json(slot: Slot, me: User | None):
        return SlotAsForeign(
            id = slot.id,
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            mine = slot.patient_id == me.id if me else False
        ).model_dump()


class MySlotAsElement(BaseModel):
    id: int
    index: int
    date: str
    startTime: str
    endTime: str
    isFinished: bool
    type: AppointmentTypeAsForeign
    category: CategoryAsForeign
    room: RoomAsPrimary
    doctor: DoctorAsForeign

    def to_json(slot: Slot):
        return MySlotAsElement(
            id = slot.id,
            index = slot.index,
            date = calc.time_to_str(slot.workday.date),
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            isFinished = datetime.now() > datetime.combine(slot.date, slot.ends_at),
            type = AppointmentTypeAsForeign.to_json(slot.type),
            category = CategoryAsForeign.to_json(slot.workday.doctor.category),
            room = RoomAsPrimary.to_json(slot.workday.doctor.office),
            doctor = DoctorAsForeign.to_json(slot.workday.doctor)
        ).model_dump()