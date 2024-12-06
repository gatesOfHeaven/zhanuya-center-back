from core.bases import BaseFactory
from .entity import AppointmentType


class Factory(BaseFactory):
    async def seed(self):
        fakes: list[AppointmentType] = [
            AppointmentType(
                name = 'visit',
                min_duration_mins = 30,
                max_duration_mins = 30
            ),
            AppointmentType(
                name = 'treatment',
                min_duration_mins = 30,
                max_duration_mins = 60
            )
        ]
        await self.flush(fakes)
        return fakes