from datetime import date

from core.bases import BaseFactory
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
    async def seed(self):
        fakes: list[Worktime] = [worktime for worktime in worktimes]
        await self.flush(fakes)
        return fakes