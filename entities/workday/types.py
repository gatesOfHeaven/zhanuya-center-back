from pydantic import BaseModel
from datetime import time

from utils.facades import calc
from entities.user import User
from entities.slot import SlotAsForeign
from .entity import Workday


class Lunch(BaseModel):
    startTime: str
    endTime: str

    def to_json(workday: Workday):
        return Lunch(
            startTime = calc.time_to_str(workday.lunch_starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(workday.lunch_ends_at, '%H:%M:%S')
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
            date = calc.time_to_str(workday.date),
            dayAtWeek = workday.day_at_week,
            startTime = calc.time_to_str(workday.starts_at),
            endTime = calc.time_to_str(workday.ends_at),
            lunch = Lunch.to_json(workday),
            slots = [SlotAsForeign.to_json(slot, me) for slot in workday.slots]
        ).model_dump()