from pydantic import BaseModel

from .entity import AppointmentType


class AppointmentTypeAsForeign(BaseModel):
    id: int
    name: str
    minDurationInMinutes: int
    maxDurationInMinutes: int

    def to_json(type: AppointmentType):
        return AppointmentTypeAsForeign(
            id = type.id,
            name = type.name,
            minDurationInMinutes = type.min_duration_mins,
            maxDurationInMinutes = type.max_duration_mins
        ).model_dump()