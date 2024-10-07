from pydantic import BaseModel

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
            stratTime = slot.starts_at,
            endTime = slot.ends_at,
            mine = slot.patient_id == me.id if me else False
        ).model_dump()