from pydantic import BaseModel

from utils.facades import calc
from entities.doctor import Doctor
from entities.category import CategoryAsForeign
from entities.office import OfficeAsForeign


class DoctorAsElement(BaseModel):
    id: int
    name: str
    surname: str
    avatarUrl: str
    age: int
    expInMonthes: int
    category: CategoryAsForeign
    office: OfficeAsForeign

    def to_json(doctor: Doctor):
        return DoctorAsElement(
            id = doctor.id,
            name = doctor.profile.name,
            surname = doctor.profile.surname,
            avatarUrl = doctor.avatar_url,
            age = calc.get_monthes(doctor.profile.birth_date),
            expInMonthes = calc.get_monthes(doctor.career_started_on),
            category = CategoryAsForeign.to_json(doctor.category),
            office = OfficeAsForeign.to_json(doctor.office)
        ).model_dump()