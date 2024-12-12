from pydantic import BaseModel, Field
from datetime import datetime

from core.bases import BaseResponse
from core.facades import calc
from entities.user import UserAsForeign
from entities.slot import Slot, AppointmentStatus
from entities.medical_record import MedicalRecord
from entities.doctor import DoctorAsForeign
from entities.category import CategoryAsForeign
from entities.room import RoomAsPrimary
from entities.appointment_type import AppointmentTypeAsForeign
from entities.payment import ReceiptAsForeign


class MedicalRecordAsForeign(BaseResponse):
    title: str
    type: str
    addedTime: str
    content: str

    @staticmethod
    def to_json(record: MedicalRecord):
        return MedicalRecordAsForeign(
            title = record.title,
            type = record.type.value,
            addedTime = calc.time_to_str(record.added_at, '%d.%m.%Y %H:%M:%S'),
            content = record.content
        ).model_dump()


class SlotAsPrimary(BaseResponse):
    id: int
    date: str
    index: int
    startTime: str
    endTime: str
    price: int
    status: AppointmentStatus
    type: AppointmentTypeAsForeign
    category: CategoryAsForeign
    room: RoomAsPrimary
    doctor: DoctorAsForeign
    patient: UserAsForeign
    receipt: ReceiptAsForeign | None
    medicalRecords: list[MedicalRecordAsForeign] | None

    @staticmethod
    def to_json(slot: Slot):
        return SlotAsPrimary(
            id = slot.id,
            date = calc.time_to_str(slot.workday.date),
            index = slot.index,
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            price = slot.price,
            status = slot.status(),
            type = AppointmentTypeAsForeign.to_json(slot.type),
            category = CategoryAsForeign.to_json(slot.workday.doctor.category),
            room = RoomAsPrimary.to_json(slot.workday.doctor.office),
            doctor = DoctorAsForeign.to_json(slot.workday.doctor),
            patient = UserAsForeign.to_json(slot.patient),
            receipt = ReceiptAsForeign.to_json(slot.payment) if slot.payment else None,
            medicalRecords = [
                MedicalRecordAsForeign.to_json(record) for record in slot.records
            ] if slot.payment is not None else None
        ).model_dump()


class MySlotAsElement(BaseResponse):
    id: int
    index: int
    date: str
    startTime: str
    endTime: str
    price: int
    isFinished: bool
    isPaid: bool
    type: AppointmentTypeAsForeign
    category: CategoryAsForeign
    room: RoomAsPrimary
    doctor: DoctorAsForeign

    @staticmethod
    def to_json(slot: Slot):
        return MySlotAsElement(
            id = slot.id,
            index = slot.index,
            date = calc.time_to_str(slot.workday.date),
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            price = slot.price,
            isFinished = datetime.now() > slot.end_datetime(),
            isPaid = slot.payment is not None,
            type = AppointmentTypeAsForeign.to_json(slot.type),
            category = CategoryAsForeign.to_json(slot.workday.doctor.category),
            room = RoomAsPrimary.to_json(slot.workday.doctor.office),
            doctor = DoctorAsForeign.to_json(slot.workday.doctor)
        ).model_dump()