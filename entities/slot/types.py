from pydantic import BaseModel, Field

from core.bases import BaseResponse
from core.facades import calc
from entities.category import CategoryAsForeign
from entities.appointment_type import AppointmentTypeAsForeign
from .entity import Slot


class MakeAppointmentReq(BaseModel):
    doctorId: int = Field(gt = 0)
    date: str = Field(pattern = r'\d{2}\.\d{2}\.\d{4}')
    typeId: int = Field(gt = 0)
    startsAt: str = Field(pattern = r'\d{2}\:\d{2}\:\d{2}')
    endsAt: str = Field(pattern = r'\d{2}\:\d{2}\:\d{2}')


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