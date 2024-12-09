from pydantic import BaseModel, Field

from core.bases import BaseResponse
from core.facades import calc
from entities.user import User


class InvitationReq(BaseModel):
    email: str = Field(min_length = 5, max_length = 50)


class PatientAsElement(BaseResponse):
    id: int
    name: str
    surname: str
    age: int
    avatarUrl: str | None

    @staticmethod
    def to_json(patient: User):
        return PatientAsElement(
            id = patient.id,
            name = patient.name,
            surname = patient.surname,
            age = calc.get_age(patient.birth_date),
            avatarUrl = None # todo
        ).model_dump()