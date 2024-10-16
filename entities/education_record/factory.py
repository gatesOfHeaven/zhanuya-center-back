from random import randint, choice
from datetime import date

from utils.bases import BaseFactory
from entities.user import User
from entities.doctor import Doctor
from entities.role import RoleID
from .entity import EducationRecord


class Factory(BaseFactory):
    async def seed(self, doctors: list[Doctor], users: list[User]):
        fakes: list[EducationRecord] = []
        managers = [user for user in users if user.role_id == RoleID.MANAGER.value]

        for doctor in doctors:
            today = date.today()
            birth_date: date = doctor.profile.birth_date
            if today.year - birth_date.year <= 18:
                continue

            start_date = self.fake.date_between(birth_date, today)
            gpa_from = randint(3, 12)
            fakes.append(EducationRecord(
                doctor = doctor,
                record_id = 1,
                organization = self.fake.company(),
                start_year = start_date.year,
                end_year = self.fake.date_between(start_date, today).year,
                gpa = 4 if self.fake.boolean(50) else randint(1, gpa_from),
                gpa_from = gpa_from,
                approved_manager = choice(managers)
            ))
        
        await self.flush(fakes)
        return fakes