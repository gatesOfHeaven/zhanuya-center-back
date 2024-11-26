from utils.bases import BaseResponse
from utils.facades import calc
from entities.category import CategoryAsForeign
from entities.slot import Slot
from entities.appointment_type import AppointmentTypeAsForeign


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