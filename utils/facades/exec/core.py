from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from typing import Callable, TypeVarTuple


scheduler = AsyncIOScheduler()
Args = TypeVarTuple('Args')


def later(
    id: str,
    job: Callable[[*Args], None],
    time: datetime,
    *args: *Args
):
    scheduler.add_job(
        id = id,
        func = job,
        trigger = DateTrigger(time),
        args = args
    )