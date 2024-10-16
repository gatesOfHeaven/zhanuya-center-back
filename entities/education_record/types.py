from pydantic import BaseModel

from .entity import EducationRecord


class EducationRecordAsForeign(BaseModel):
    id: int
    organization: str
    startYear: int
    endYear: int
    gpa: float
    gpaFrom: int
    
    def to_json(record: EducationRecord):
        return EducationRecordAsForeign(
            id = record.record_id,
            organization = record.organization,
            startYear = record.start_year,
            endYear = record.end_year,
            gpa = record.gpa,
            gpaFrom = record.gpa_from
        ).model_dump()