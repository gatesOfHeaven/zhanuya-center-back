from pydantic import BaseModel
from datetime import date

from utils.facades import calc
from entities.user.entity import User
    

class UserAsPrimary(BaseModel):
    id: int
    name: str
    surname: str
    gender: str
    birthDate: str
    age: int
    email: str
    iin: str
    role: str

    def to_json(user: User):
        birth_date: date = user.birth_date
        return UserAsPrimary(
            id = user.id,
            name = user.name,
            surname = user.surname,
            gender = user.gender,
            birthDate = calc.time_to_str(birth_date),
            age = calc.get_age(user.birth_date),
            email = user.email,
            iin = user.iin,
            role = user.role.name
        ).model_dump()
    

class PatientAsForeign(BaseModel):
    id: int
    name: str
    surname: str

    def to_json(user: User):
        return PatientAsForeign(
            id = user.id,
            name = user.name,
            surname = user.surname
        ).model_dump()