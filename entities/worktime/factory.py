from datetime import date

from utils.bases import BaseFactory
from .entity import Worktime


worktimes = [
    Worktime(
        start_date = date(2022, 2, 7),
        end_date = date(2023, 7, 2),
        starts_at = 7,
        ends_at = 20
    ),
    Worktime(
        start_date = date(2023, 7, 3),
        end_date = date(2024, 5, 20),
        starts_at = 8,
        ends_at = 19
    ),
    Worktime(
        start_date = date(2024, 5, 21),
        starts_at = 8,
        ends_at = 20
    )
]


class Factory(BaseFactory):
    fakes: list[Worktime]

    async def seed(self):
        self.fakes = []

        for worktime in worktimes:
            self.fakes.append(worktime)
            self.db.add(worktime)
        await self.flush()
        return self.fakes