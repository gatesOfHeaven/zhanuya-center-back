from utils.bases import BaseResponse
from utils.facades import calc
from entities.doctor import DoctorAsForeign
from entities.slot import SlotAsForeign
from entities.medical_record import MedicalRecord


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