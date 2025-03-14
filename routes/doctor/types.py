from core.bases import BaseResponse
from core.facades import calc
from entities.appointment_type import AppointmentTypeAsForeign
from entities.worktime import Worktime, WorktimeAsForeign
from entities.workday import Workday
from entities.user import User, Gender, UserAsForeign
from entities.slot import Slot, AppointmentStatus
from entities.lunch import LunchAsForeign


class ScheduleSlot(BaseResponse):
    id: int
    startTime: str
    endTime: str
    type: AppointmentTypeAsForeign
    status:  AppointmentStatus
    patient: UserAsForeign

    @staticmethod
    def to_json(slot: Slot):
        return ScheduleSlot(
            id = slot.id,
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            type = AppointmentTypeAsForeign.to_json(slot.type),
            status = slot.status(),
            patient = UserAsForeign.to_json(slot.patient),
        ).model_dump()


class ScheduleDay(BaseResponse):
    date: str
    dayAtWeek: int
    startTime: str
    endTime: str
    lunch: LunchAsForeign | None
    slots: list[ScheduleSlot]

    @staticmethod
    def to_json(workday: Workday):
        time_format = '%H:%M:%S'
        return ScheduleDay(
            date = calc.time_to_str(workday.date),
            dayAtWeek = workday.day_at_week,
            startTime = calc.time_to_str(workday.starts_at, time_format),
            endTime = calc.time_to_str(workday.ends_at, time_format),
            lunch = LunchAsForeign.to_json(workday.lunch) if workday.lunch else None,
            slots = [ScheduleSlot.to_json(slot) for slot in workday.slots]
        ).model_dump() 


class MySchedule(BaseResponse):
    worktime: WorktimeAsForeign | None
    schedule: list[ScheduleDay]

    @staticmethod
    def to_json(
        worktime: Worktime | None,
        schedule: list[Workday]
    ):
        return MySchedule(
            worktime = WorktimeAsForeign.to_json(worktime) if worktime else None,
            schedule = [
                ScheduleDay.to_json(workday)
                for workday in schedule
            ]
        ).model_dump()


class PatientAsPrimary(BaseResponse):
    id: int
    name: str
    surname: str
    gender: Gender
    birth_date: str

    @staticmethod
    def to_json(patient: User):
        return PatientAsPrimary(
            id = patient.id,
            name = patient.name,
            surname = patient.surname,
            gender = patient.gender,
            birth_date = calc.time_to_str(patient.birth_date)
        ).model_dump()