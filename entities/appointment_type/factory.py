from utils.bases import BaseFactory
from .entity import AppointmentType


type_names = [
    'visit',
    'treatment'
]


class Factory(BaseFactory):
    async def seed(self):
        fakes: list[AppointmentType] = [
            AppointmentType(name = name)
            for name in type_names
        ]
        await self.flush(fakes)
        return fakes