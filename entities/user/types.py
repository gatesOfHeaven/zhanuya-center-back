from core.bases import BaseResponse
from core.facades import calc
from entities.user.entity import User


class UserAsPrimary(BaseResponse):
    id: int
    name: str
    surname: str
    gender: str
    birthDate: str
    age: int
    email: str
    iin: str
    role: str
    buildingId: int | None

    @staticmethod
    def to_json(user: User):
        return UserAsPrimary(
            id = user.id,
            name = user.name,
            surname = user.surname,
            gender = user.gender.value,
            birthDate = calc.time_to_str(user.birth_date),
            age = calc.get_age(user.birth_date),
            email = user.email,
            iin = user.iin,
            role = user.role_type.value,
            buildingId = (
                user.as_manager.building_id if user.as_manager else
                user.as_doctor.office.building_id if user.as_doctor else
                None
            )
        ).model_dump()


class UserAsForeign(BaseResponse):
    id: int
    name: str
    surname: str

    @staticmethod
    def to_json(user: User):
        return UserAsForeign(
            id = user.id,
            name = user.name,
            surname = user.surname
        ).model_dump()