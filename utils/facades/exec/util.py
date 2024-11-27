from apscheduler.jobstores.base import JobLookupError
from datetime import timedelta

from utils.facades import mail, calc
from .core import later, remove
from entities.slot import Slot


def job_id(appointment: Slot) -> str:
    return f'slot-{appointment.id}-patient'


def schedule_appointment_notification(appointment: Slot, minutes: int = 380):
    async def notify_about_appointment(appointment: Slot):
        profile = appointment.workday.doctor.profile
        office = appointment.workday.doctor.office
        print('sent about', appointment.id, 'to', appointment.patient_id)
        await mail.send(
            appointment.patient.email,
            'You have an Appointment',
            f'Your doctor {profile.name} {profile.surname} will be waiting for you at the address {office.building.address}, office {office.title} at {calc.time_to_str(appointment.starts_at, '%H:%M')}'
        )

    later(
        id = job_id(appointment),
        job = notify_about_appointment,
        time = appointment.start_datetime() - timedelta(minutes = minutes),
        args = (appointment,)
    )


def unschedule_appointment_notification(appointment: Slot):
    try:
        remove(job_id(appointment))
        print('deleted', job_id(appointment))
    except JobLookupError as e: print('skip', e)