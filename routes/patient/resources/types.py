from pydantic import BaseModel

from entities.user import User
from entities.doctor import Doctor
from entities.category import Category, CategoryAsForeign
from entities.doctor import Doctor
from entities.building import Building, BuildingAsForeign


class DoctorsAsResource(BaseModel):
    id: int
    name: str
    surname: str

    def to_json(doctor: User):
        return DoctorsAsResource(
            id = doctor.id,
            name = doctor.name,
            surname = doctor.surname
        ).model_dump()


class ResourcesRes(BaseModel):
    doctors: list[DoctorsAsResource]
    categories: list[CategoryAsForeign]
    offices: list[BuildingAsForeign]

    def to_json(
        doctors: list[Doctor],
        categories: list[Category],
        offices: list[Building]
    ):
        return ResourcesRes(
            doctors = [DoctorsAsResource.to_json(doctor.profile) for doctor in doctors],
            categories = [CategoryAsForeign.to_json(category) for category in categories],
            offices = [BuildingAsForeign.to_json(office) for office in offices]
        ).model_dump()