from pydantic import BaseModel

from utils.facades import calc
from .entity import Lunch


class LunchAsForeign(BaseModel):
    startTime: str
    endTime: str

    def to_json(lunch: Lunch):
        time_format = '%H:%M:%S'
        return LunchAsForeign(
            startTime = calc.time_to_str(lunch.starts_at, time_format),
            endTime = calc.time_to_str(lunch.ends_at, time_format)
        ).model_dump()