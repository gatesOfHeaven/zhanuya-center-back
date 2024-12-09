from core.bases import BaseResponse
from core.facades import calc
from entities.user import User, UserAsForeign
from entities.worktime import Worktime, WorktimeAsForeign
from entities.workday import Workday
from entities.appointment_type import AppointmentTypeAsForeign
from entities.slot import Slot, AppointmentStatus
from entities.lunch import LunchAsForeign


class ScheduleSlot(BaseResponse):
    id: int
    startTime: str
    endTime: str
    type: AppointmentTypeAsForeign
    status:  AppointmentStatus
    patient: UserAsForeign | None

    @staticmethod
    def to_json(slot: Slot, show_patients: bool):
        return ScheduleSlot(
            id = slot.id,
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            type = AppointmentTypeAsForeign.to_json(slot.type),
            status = slot.status(),
            patient = UserAsForeign.to_json(slot.patient) if show_patients else None,
        ).model_dump()
    

class ScheduleDay(BaseResponse):
    date: str
    dayAtWeek: int
    startTime: str
    endTime: str
    lunch: LunchAsForeign | None
    slots: list[ScheduleSlot]

    @staticmethod
    def to_json(workday: Workday, show_patients: bool):
        time_format = '%H:%M:%S'
        return ScheduleDay(
            date = calc.time_to_str(workday.date),
            dayAtWeek = workday.day_at_week,
            startTime = calc.time_to_str(workday.starts_at, time_format),
            endTime = calc.time_to_str(workday.ends_at, time_format),
            lunch = LunchAsForeign.to_json(workday.lunch) if workday.lunch else None,
            slots = [ScheduleSlot.to_json(slot, show_patients) for slot in workday.slots]
        ).model_dump() 
    

class ScheduleRes(BaseResponse):
    worktime: WorktimeAsForeign | None
    showPatients: bool
    schedule: list[ScheduleDay]

    @staticmethod
    def to_json(
        worktime: Worktime | None,
        schedule: list[Workday],
        show_patients: bool
    ):
        return ScheduleRes(
            worktime = WorktimeAsForeign.to_json(worktime) if worktime else None,
            showPatients = show_patients,
            schedule = [
                ScheduleDay.to_json(workday, show_patients)
                for workday in schedule
            ]
        ).model_dump()