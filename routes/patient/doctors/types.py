from pydantic import BaseModel
from datetime import timedelta

from core.bases import BaseResponse
from core.facades import calc
from entities.user import User
from entities.doctor import Doctor, DoctorAsPrimary
from entities.category import CategoryAsForeign
from entities.room import RoomAsPrimary
from entities.price import PriceAsPrimary
from entities.worktime import Worktime, WorktimeAsForeign
from entities.workday import Workday
from entities.slot import Slot
from entities.lunch import LunchAsForeign


class ScheduleSlot(BaseResponse):
    id: int
    startTime: str
    endTime: str
    mine: bool

    @staticmethod
    def to_json(slot: Slot, me: User | None = None):
        return ScheduleSlot(
            id = slot.id,
            startTime = calc.time_to_str(slot.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(slot.ends_at, '%H:%M:%S'),
            mine = slot.patient_id == me.id if me else False
        ).model_dump()
    

class ScheduleDay(BaseResponse):
    date: str
    dayAtWeek: int
    startTime: str
    endTime: str
    lunch: LunchAsForeign | None
    slots: list[ScheduleSlot]

    @staticmethod
    def to_json(workday: Workday, me: User | None):
        time_format = '%H:%M:%S'
        return ScheduleDay(
            date = calc.time_to_str(workday.date),
            dayAtWeek = workday.day_at_week,
            startTime = calc.time_to_str(workday.starts_at, time_format),
            endTime = calc.time_to_str(workday.ends_at, time_format),
            lunch = LunchAsForeign.to_json(workday.lunch) if workday.lunch else None,
            slots = [ScheduleSlot.to_json(slot, me) for slot in workday.slots]
        ).model_dump() 
    

class ScheduleRes(BaseResponse):
    worktime: WorktimeAsForeign | None
    schedule: list[ScheduleDay]

    @staticmethod
    def to_json(
        worktime: Worktime | None,
        schedule: list[Workday],
        me: User | None
    ):
        return ScheduleRes(
            worktime = WorktimeAsForeign.to_json(worktime) if worktime else None,
            schedule = [
                ScheduleDay.to_json(workday, me)
                for workday in schedule
            ]
        ).model_dump()


class DoctorAsElement(BaseResponse):
    id: int
    name: str
    surname: str
    avatarUrl: str
    age: int
    visitPrice: int
    expInMonthes: int
    category: CategoryAsForeign
    office: RoomAsPrimary

    @staticmethod
    def to_json(doctor: Doctor):
        visitPrice = next((price.cost for price in doctor.price_list if price.type_id == 1), None)
        return DoctorAsElement(
            id = doctor.id,
            name = doctor.profile.name,
            surname = doctor.profile.surname,
            avatarUrl = doctor.avatar_url,
            age = calc.get_age(doctor.profile.birth_date),
            visitPrice = visitPrice,
            expInMonthes = calc.get_monthes(doctor.career_started_on),
            category = CategoryAsForeign.to_json(doctor.category),
            office = RoomAsPrimary.to_json(doctor.office)
        ).model_dump()
    

class DoctorAsPage(BaseResponse):
    profile: DoctorAsPrimary
    worktime: WorktimeAsForeign
    schedule: list[ScheduleDay]

    @staticmethod
    def to_json(
        doctor: Doctor,
        worktime: Worktime,
        schedule: list[Workday],
        me: User | None
    ):
        return DoctorAsPage(
            profile = DoctorAsPrimary.to_json(doctor),
            worktime = WorktimeAsForeign.to_json(worktime),
            schedule = [
                ScheduleDay.to_json(workday, me)
                for workday in schedule
            ]
        ).model_dump()
    

class FreeSlotAsElement(BaseModel):
    startTime: str
    endTime: str

    def duration(self) -> timedelta:
        format = '%H:%M:%S'
        return calc.str_to_time(self.endTime, format) - calc.str_to_time(self.startTime, format)


class FreeSlotsRes(BaseResponse):
    freeSlots: list[FreeSlotAsElement]
    priceList: list[PriceAsPrimary]

    @staticmethod
    def to_json(freeSlots: list[FreeSlotAsElement], workday: Workday):
        return FreeSlotsRes(
            freeSlots = freeSlots,
            priceList = [PriceAsPrimary.to_json(price) for price in workday.doctor.price_list]
        ).model_dump()