from apscheduler.jobstores.base import JobLookupError
from datetime import datetime, timedelta
from aiofiles import open as asyncopen

from config.rootdir import LOG_DIR
from core.facades import mail, calc
from core.facades.exec import start, later, remove
from entities.slot import Slot


def job_id(appointment: Slot) -> str:
    return f'slot-{appointment.id}-patient'


def schedule_appointment_notification(appointment: Slot, hours: int = 3, save_log: bool = True):
    async def notify_about_appointment(appointment: Slot):
        office = appointment.workday.doctor.office
        if save_log:
            async with asyncopen(LOG_DIR / 'notified-appointments.txt', 'a') as file:
                await file.write(f'\n{datetime.now()}: {appointment.id}')
        await mail.send(
            appointment.patient.email,
            'You have an Appointment',
            f'Your doctor {appointment.workday.doctor.profile.fullname()} will be waiting for you at the address '
            f'{office.building.address}, office {office.title} at {calc.time_to_str(appointment.starts_at, '%H:%M')}'
        )

    later(
        id = job_id(appointment),
        job = notify_about_appointment,
        time = appointment.start_datetime() - timedelta(hours = hours),
        args = (appointment,)
    )


async def unschedule_appointment_notification(appointment: Slot):
    error_msg = None
    try: remove(job_id(appointment))
    except JobLookupError as e: error_msg = e
    async with asyncopen(LOG_DIR / ('errors.txt' if error_msg else'canceled-appointments.txt'), 'a') as file:
        await file.write(f'\n{datetime.now()}: {appointment.id} {appointment.date} {appointment.starts_at}-{appointment.ends_at} d={appointment.doctor_id} p={appointment.patient_id}')