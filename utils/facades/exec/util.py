# from apscheduler.jobstores.base import JobLookupError
# from datetime import timedelta

# from utils.facades import mail, calc
# from .core import later, remove, all
# from entities.slot import Slot


# def job_id(appointment: Slot) -> str:
#     return f'slot[{appointment.id}]'


# def schedule_appointment_notification(appointment: Slot, minutes: int = 380):
#     async def notify_about_appointment(appointment: Slot):
#         profile = appointment.workday.doctor.profile
#         office = appointment.workday.doctor.office
#         print('sent to', appointment.patient_id)
#         await mail.send(
#             appointment.patient.email,
#             'You have an Appointment',
#             f'Your doctor {profile.name} {profile.surname} will be waiting for you at the address {office.building.address}, office {office.title} at {calc.time_to_str(appointment.starts_at, '%H:%M')}'
#         )

#     later(
#         id = job_id(appointment),
#         job = notify_about_appointment,
#         time = appointment.start_datetime() - timedelta(minutes = minutes),
#         args = (appointment,)
#     )
#     print('scheduled for', appointment)
#     all()


# def unschedule_appointment_notification(appointment: Slot):
#     try:
#         remove(job_id(appointment))
#         print('deleted', job_id(appointment))
#         all()
#     except JobLookupError as e: print('skip', e)
from fastapi import BackgroundTasks
from celery import Celery
from celery.result import AsyncResult
from datetime import datetime, timedelta, time
from typing import Protocol, Callable, Self

from utils.facades import mail, calc
from entities.slot import Slot


queue = Celery(
    'tasks',
    broker = 'redis://localhost:6379/0',
    backend = 'redis://localhost:6379/0'
)


@queue.task
async def notify_about_appointment(
    id: int,
    email: str,
    name: str,
    surname: str,
    address: str,
    room: str,
    start_time: time
):
    print('sent to', id)
    await mail.send(
        email,
        'You have an Appointment',
        f'Your doctor {name} {surname} will be waiting for you at the address {address}, office {room} at {calc.time_to_str(start_time, '%H:%M')}'
    )


def task_id(appointment: Slot) -> str:
    return f'slot[{appointment.id}]'



def schedule_appointment_notification(appointment: Slot, minutes: int = 30):
    result: AsyncResult = notify_about_appointment.apply_async(
    args=[
        appointment.patient_id,
        appointment.patient.email,
        appointment.patient.name,
        appointment.patient.surname,
        appointment.workday.doctor.office.building.address,
        appointment.workday.doctor.office.title,
        appointment.starts_at
    ],
    task_id=task_id(appointment),
    eta=appointment.start_datetime() - timedelta(minutes=minutes)
)

    print(result.id, result.args, result.as_list())



def unschedule_appointment_notification(appointment: Slot):
    task = AsyncResult(id = task_id(appointment), app = queue)
    if task.ready():
        print(f"Task {task_id} already completed.")
    else:
        task.revoke(terminate=True)
        print(f"Task {task_id} has been revoked and will not be executed.")