from core.bases import BaseResponse
from .entity import AppointmentType


class AppointmentTypeAsPrimary(BaseResponse):
    id: int
    name: str
    minDurationInMinutes: int
    maxDurationInMinutes: int

    @staticmethod
    def to_json(type: AppointmentType):
        return AppointmentTypeAsPrimary(
            id = type.id,
            name = type.name,
            minDurationInMinutes = type.min_duration_mins,
            maxDurationInMinutes = type.max_duration_mins
        ).model_dump()


class AppointmentTypeAsForeign(BaseResponse):
    id: int
    name: str

    @staticmethod
    def to_json(type: AppointmentType):
        return AppointmentTypeAsForeign(
            id = type.id,
            name = type.name
        ).model_dump()