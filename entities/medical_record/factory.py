from random import choice, randint
from datetime import timedelta

from core.bases import BaseFactory
from entities.slot import Slot
from entities.manager import Manager
from .entity import MedicalRecord
from .values import MedicalRecordType


class Factory(BaseFactory):
    async def seed(self, slots: list[Slot]):
        fakes: list[MedicalRecord] = [MedicalRecord(
            slot = slot,
            type = choice(list(MedicalRecordType)),
            added_at = slot.end_datetime() + timedelta(seconds = randint(-1200, 1800)),
            title = ' '.join(self.fake.words(randint(1, 5))),
            content = ' '.join(self.fake.words(randint(10, 50)))
        ) for slot in slots if slot.payment is not None]

        await self.flush(fakes)
        return fakes