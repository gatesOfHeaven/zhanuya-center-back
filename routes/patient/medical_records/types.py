from utils.bases import BaseResponse
from utils.facades import calc
from entities.doctor import DoctorAsForeign
from entities.category import CategoryAsForeign
from entities.slot import Slot
from entities.appointment_type import AppointmentTypeAsForeign
from entities.medical_record import MedicalRecord


class SlotAsForeign(BaseResponse):
    id: int
    date: str
    startTime: str
    endTime: str
    type: AppointmentTypeAsForeign
    category: CategoryAsForeign

    @staticmethod
    def to_json(slot: Slot):
        return SlotAsForeign(
            id = slot.id,
            date = calc.time_to_str(slot.date),
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            type = AppointmentTypeAsForeign.to_json(slot.type),
            category = CategoryAsForeign.to_json(slot.workday.doctor.category)
        ).model_dump()


class MedicalRecordAsElement(BaseResponse):
    type: str
    title: str
    content: str
    addedTime: str
    doctor: DoctorAsForeign
    appointment: SlotAsForeign

    @staticmethod
    def to_json(record: MedicalRecord):
        return MedicalRecordAsElement(
            type = record.type.value,
            title = record.title,
            content = record.content,
            addedTime = calc.time_to_str(record.added_at, '%d.%m.%Y %H:%M:%S'),
            doctor = DoctorAsForeign.to_json(record.slot.workday.doctor),
            appointment = SlotAsForeign.to_json(record.slot)
        ).model_dump()