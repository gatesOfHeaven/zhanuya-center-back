from datetime import timedelta

from utils.facades import exec, mail, calc
from entities.slot import Slot


def job_id(appointment: Slot) -> str:
    return f'slot[{appointment.id}]'


def schedule_appointment_notification(appointment: Slot, minutes: int = 30):
    async def notify_about_appointment(appointment: Slot):
        profile = appointment.workday.doctor.profile
        office = appointment.workday.doctor.office
        await mail.send(
            appointment.patient.email,
            'You have an Appointment',
            f'Your doctor {profile.name} {profile.surname} will be waiting for you at the address {office.building.address}, office {office.id} at {calc.time_to_str(appointment.starts_at, '%H:%M')}'
        )
        
    exec.later(
        id = job_id(appointment),
        job = notify_about_appointment,
        time = appointment.starts_at - timedelta(minutes = minutes),
        args = appointment
    )


def unschedule_appointment_notification(appointment: Slot):
    exec.remove(job_id(appointment))