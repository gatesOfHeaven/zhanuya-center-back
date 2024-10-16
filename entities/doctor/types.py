from pydantic import BaseModel

from utils.facades import calc
from entities.category import CategoryAsForeign
from entities.room import RoomAsPrimary
from entities.price import PriceAsPrimary
from entities.experience_record import ExperienceRecordAsForeign
from entities.education_record import EducationRecordAsForeign
from .entity import Doctor


class DoctorAsPrimary(BaseModel):
    id: int
    name: str
    surname: str
    avatarUrl: str
    age: int
    expInMonthes: int
    category: CategoryAsForeign
    office: RoomAsPrimary
    price_list: list[PriceAsPrimary]
    experience: list[ExperienceRecordAsForeign]
    education: list[EducationRecordAsForeign]

    def to_json(doctor: Doctor):
        return DoctorAsPrimary(
            id = doctor.id,
            name = doctor.profile.name,
            surname = doctor.profile.surname,
            avatarUrl = doctor.avatar_url,
            age = calc.get_age(doctor.profile.birth_date),
            expInMonthes = calc.get_monthes(doctor.career_started_on),
            category = CategoryAsForeign.to_json(doctor.category),
            office = RoomAsPrimary.to_json(doctor.office),
            price_list = [
                PriceAsPrimary.to_json(price)
                for price in doctor.price_list
            ],
            experience = [
                ExperienceRecordAsForeign.to_json(record)
                for record in doctor.experience
            ],
            education = [
                EducationRecordAsForeign.to_json(record)
                for record in doctor.education
            ]
        ).model_dump()
