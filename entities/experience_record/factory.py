from random import randint, choice
from datetime import date

from utils.bases import BaseFactory
from entities.user import User
from entities.doctor import Doctor
from entities.category import Category
from entities.role import RoleID
from .entity import ExperienceRecord


class Factory(BaseFactory):
    async def seed(
        self,
        doctors: list[Doctor],
        users: list[User],
        categories: list[Category]
    ):
        fakes: list[ExperienceRecord] = []
        managers = [user for user in users if user.role_id == RoleID.MANAGER.value]

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