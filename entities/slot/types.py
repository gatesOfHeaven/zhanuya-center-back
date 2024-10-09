from pydantic import BaseModel
from datetime import time

from utils.facades import calc
from entities.user import User
from .entity import Slot


class SlotAsForeign(BaseModel):
    id: int
    stratTime: str
    endTime: str
    mine: bool

    def to_json(slot: Slot, me: User | None):
        return SlotAsForeign(
            id = slot.id,
            stratTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            mine = slot.patient_id == me.id if me else False
        ).model_dump()