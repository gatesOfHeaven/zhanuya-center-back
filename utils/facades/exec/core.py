# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.date import DateTrigger
# from apscheduler.job import Job
# from datetime import datetime, timedelta
# from typing import Callable, TypeVarTuple, Coroutine
# from asyncio import create_task 
# from pytz import timezone
# import logging

# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.INFO)


# scheduler = AsyncIOScheduler(timezone = timezone('Asia/Almaty'))
# scheduler.start()
# Args = TypeVarTuple('Args')


# def later(
#     id: str,
#     job: Callable[[*Args], Coroutine],
#     time: datetime,
#     args: tuple[*Args]
# ):
#     print(datetime.now(), time)
#     job: Job = scheduler.add_job(
#         id = id,
#         func = job,
#         trigger = DateTrigger(run_date=(datetime.now() + timedelta(seconds = 15))),
#         args = list(args)
#     )
#     print(job.trigger)


# def all():
#     for job in scheduler.get_jobs():
#         job: Job
#         print(job.id, job.args, job.trigger)


# def remove(id: str):
#     scheduler.remove_job(id)