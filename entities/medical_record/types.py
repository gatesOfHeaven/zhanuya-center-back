from pydantic import BaseModel

from utils.facades import calc
from entities.doctor import DoctorAsForeign
from entities.category import CategoryAsForeign
from .entity import MedicalRecord


class MedicalRecordAsElement(BaseModel):
    type: str
    title: str
    content: str
    appointmentType: str
    addedTime: str
    doctor: DoctorAsForeign
    category: CategoryAsForeign

    @staticmethod
    def to_json(record: MedicalRecord):
        doctor = record.slot.workday.doctor
        return MedicalRecordAsElement(
            type = record.type.value,
            title = record.title,
            content = record.content,
            appointmentType = record.slot.type.name,
            addedTime = calc.time_to_str(record.added_at, '%d.%m.%Y %H:%M'),
            doctor = DoctorAsForeign.to_json(doctor),
            category = CategoryAsForeign.to_json(doctor.category)
        ).model_dump()