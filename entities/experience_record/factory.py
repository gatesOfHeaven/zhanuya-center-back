from random import randint, choice
from datetime import date

from core.bases import BaseFactory
from entities.doctor import Doctor
from entities.manager import Manager
from entities.category import Category
from .entity import ExperienceRecord


class Factory(BaseFactory):
    async def seed(
        self,
        doctors: list[Doctor],
        managers: list[Manager],
        categories: list[Category]
    ):
        fakes: list[ExperienceRecord] = []
        for doctor in doctors:
            today = date.today()
            birth_date: date = doctor.profile.birth_date
            if today.year - birth_date.year <= 18:
                continue

            start_date = self.fake.date_between(birth_date, today)
            fakes.append(ExperienceRecord(
                doctor = doctor,
                record_id = 1,
                organization = self.fake.company(),
                start_date = start_date,
                end_date = self.fake.date_between(start_date, today),
                position = choice(categories).title,
                hours_at_day = randint(3, 8),
                approved_manager = choice(managers)
            ))
        
        await self.flush(fakes)
        return fakes