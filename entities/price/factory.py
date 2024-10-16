from random import randint

from utils.bases import BaseFactory
from entities.doctor import Doctor
from entities.appointment_type import AppointmentType
from .entity import Price


class Factory(BaseFactory):
    async def seed(self, doctors: list[Doctor], types: list[AppointmentType]):
        fakes: list[Price] = []
        for doctor in doctors:
            for type in types:
                if self.fake.boolean(75):
                    fakes.append(Price(
                        doctor = doctor,
                        appointment_type = type,
                        half_hour_price = randint(5, 25) * 1000
                    ))        
        await self.flush(fakes)
        return fakes