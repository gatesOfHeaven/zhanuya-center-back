# from celery import Celery
# from celery.result import AsyncResult
# from datetime import datetime, timedelta
# from typing import Protocol, Callable, Self

# from utils.facades import mail, calc
# from entities.slot import Slot


# queue = Celery(
#     'tasks',
#     broker = 'redis://localhost:6379/0',
#     backend = 'redis://localhost:6379/0'
# )


# @queue.task
# async def notify_about_appointment(appointment: Slot):
#     profile = appointment.workday.doctor.profile
#     office = appointment.workday.doctor.office
#     print('sent to', appointment.patient_id)
#     await mail.send(
#         appointment.patient.email,
#         'You have an Appointment',
#         f'Your doctor {profile.name} {profile.surname} will be waiting for you at the address {office.building.address}, office {office.title} at {calc.time_to_str(appointment.starts_at, '%H:%M')}'
#     )


# def task_id(appointment: Slot) -> str:
#     return f'slot[{appointment.id}]'



# def schedule_appointment_notification(appointment: Slot, minutes: int = 30):
#     result: AsyncResult = notify_about_appointment.apply_async(
#         task_id = task_id(appointment),
#         args = [appointment],
#         eta = appointment.start_datetime() - timedelta(minutes = 30)
#     )
#     print(result.id)