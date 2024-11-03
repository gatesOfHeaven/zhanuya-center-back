from pydantic import BaseModel

from utils.facades import calc
from entities.user import User
from entities.lunch import LunchAsForeign
from entities.slot import SlotAsForeign
from .entity import Workday
    

class WorkdayAsPrimary(BaseModel):
    date: str
    dayAtWeek: int
    startTime: str
    endTime: str
    lunch: LunchAsForeign | None
    slots: list[SlotAsForeign]

    @staticmethod
    def to_json(workday: Workday, me: User | None):
        time_format = '%H:%M:%S'
        return WorkdayAsPrimary(
            date = calc.time_to_str(workday.date),
            dayAtWeek = workday.day_at_week,
            startTime = calc.time_to_str(workday.starts_at, time_format),
            endTime = calc.time_to_str(workday.ends_at, time_format),
            lunch = LunchAsForeign.to_json(workday.lunch) if workday.lunch else None,
            slots = [SlotAsForeign.to_json(slot, me) for slot in workday.slots]
        ).model_dump()