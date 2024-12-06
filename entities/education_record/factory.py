from random import randint, choice
from datetime import date

from core.bases import BaseFactory
from entities.doctor import Doctor
from entities.manager import Manager
from .entity import EducationRecord


class Factory(BaseFactory):
    async def seed(self, doctors: list[Doctor], managers: list[Manager]):
        fakes: list[EducationRecord] = []
        for doctor in doctors:
            today = date.today()
            birth_date: date = doctor.profile.birth_date
            start_date = self.fake.date_between(birth_date, today)
            gpa_from = 4 if self.fake.boolean(75) else randint(3, 12)
            fakes.append(EducationRecord(
                doctor = doctor,
                record_id = 1,
                organization = self.fake.company(),
                speciality = doctor.category.title,
                start_year = start_date.year,
                end_year = self.fake.date_between(start_date, today).year,
                gpa = randint(1, gpa_from),
                gpa_from = gpa_from,
                approved_manager = choice(managers)
            ))
        
        await self.flush(fakes)
        return fakes