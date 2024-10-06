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
    role: str

    def resource(user: User):
        birth_date: date = user.birth_date
        return UserAsPrimary(
            id = user.id,
            name = user.name,
            surname = user.surname,
            gender = user.gender,
            birthDate = birth_date.strftime('%d-%m-%Y'),
            age = calc.get_age(user.birth_date),
            email = user.email,
            role = user.role.name
        ).model_dump()