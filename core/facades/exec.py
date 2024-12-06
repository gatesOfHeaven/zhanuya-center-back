from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from typing import Callable, TypeVarTuple, Coroutine


scheduler = AsyncIOScheduler()
Args = TypeVarTuple('Args')


def start():
    scheduler.start()


def later(
    id: str,
    job: Callable[[*Args], Coroutine],
    time: datetime,
    args: tuple[*Args]
):
    scheduler.add_job(
        id = id,
        func = job,
        trigger = DateTrigger(time),
        args = list(args),
        replace_existing = True
    )


def remove(id: str):
    scheduler.remove_job(id)