from utils.bases import BaseResponse
from utils.facades import calc
from .entity import ExperienceRecord


class ExperienceRecordAsForeign(BaseResponse):
    id: int
    organization: str
    startDate: str
    endDate: str
    position: str
    hoursAtDay: int
    
    @staticmethod
    def to_json(record: ExperienceRecord):
        return ExperienceRecordAsForeign(
            id = record.record_id,
            organization = record.organization,
            startDate = calc.time_to_str(record.start_date),
            endDate = calc.time_to_str(record.end_date),
            position = record.position,
            hoursAtDay = record.hours_at_day
        ).model_dump()