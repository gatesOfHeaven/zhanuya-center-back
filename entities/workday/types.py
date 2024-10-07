from pydantic import BaseModel

from entities.user import User
from entities.slot import SlotAsForeign
from .entity import Workday


class Lunch(BaseModel):
    startTime: str
    endTime: str

    def to_json(workday: Workday):
        return Lunch(
            startTime = workday.lunch_starts_at,
            endTime = workday.lunch_ends_at
        ).model_dump()
    

class WorkdayAsPrimary(BaseModel):
    date: str
    dayAtWeek: int
    startTime: str
    endTime: str
    lunch: Lunch
    slots: list[SlotAsForeign]

    def to_json(workday: Workday, me: User | None):
        return WorkdayAsPrimary(
            date = workday.date,
            dayAtWeek = workday.day_at_week,
            startTime = workday.starts_at,
            endTime = workday.ends_at,
            lunch = Lunch.to_json(workday),
            slots = [SlotAsForeign.to_json(slot, me) for slot in workday.slots]
        ).model_dump()