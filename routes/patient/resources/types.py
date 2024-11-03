from pydantic import BaseModel

from entities.user import User
from entities.doctor import Doctor
from entities.category import Category, CategoryAsForeign
from entities.doctor import Doctor
from entities.building import Building, BuildingAsForeign
from entities.appointment_type import AppointmentType, AppointmentTypeAsPrimary


class DoctorsAsResource(BaseModel):
    id: int
    name: str
    surname: str

    @staticmethod
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
    appointment_types: list[AppointmentTypeAsPrimary]

    @staticmethod
    def to_json(
        doctors: list[Doctor],
        categories: list[Category],
        offices: list[Building],
        appointment_types: list[AppointmentType]
    ):
        return ResourcesRes(
            doctors = [DoctorsAsResource.to_json(doctor.profile) for doctor in doctors],
            categories = [CategoryAsForeign.to_json(category) for category in categories],
            offices = [BuildingAsForeign.to_json(office) for office in offices],
            appointment_types = [
                AppointmentTypeAsPrimary.to_json(type)
                for type in appointment_types
            ]
        ).model_dump()