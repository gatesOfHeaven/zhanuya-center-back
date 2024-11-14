from random import choice, randint
from datetime import timedelta

from utils.bases import BaseFactory
from entities.slot import Slot
from entities.manager import Manager
from .entity import MedicalRecord
from .values import MedicalRecordType


class Factory(BaseFactory):
    async def seed(self, slots: list[Slot], managers: list[Manager]):
        fakes: list[MedicalRecord] = [MedicalRecord(
            slot = slot,
            type = choice(list(MedicalRecordType)),
            added_at = slot.end_datetime() + timedelta(seconds = randint(-1200, 1800)),
            title = ' '.join(self.fake.words(randint(1, 5))),
            content = ' '.join(self.fake.words(randint(10, 50))),
            approved_manager = choice([
                manager for manager in managers
                if manager.building_id == slot.workday.doctor.office.building_id
            ]) if self.fake.boolean(95) else None
        ) for slot in slots if slot.payment is not None]

        await self.flush(fakes)
        return fakes