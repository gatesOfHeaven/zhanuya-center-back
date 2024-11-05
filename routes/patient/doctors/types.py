from pydantic import BaseModel
from datetime import timedelta

from utils.facades import calc
from entities.user import User
from entities.doctor import Doctor, DoctorAsPrimary
from entities.category import CategoryAsForeign
from entities.room import RoomAsPrimary
from entities.price import PriceAsPrimary
from entities.worktime import Worktime, WorktimeAsForeign
from entities.workday import Workday, WorkdayAsPrimary


class DoctorAsElement(BaseModel):
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
    

class DoctorAsPage(BaseModel):
    profile: DoctorAsPrimary
    worktime: WorktimeAsForeign
    schedule: list[WorkdayAsPrimary]

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
                WorkdayAsPrimary.to_json(workday, me)
                for workday in schedule
            ]
        ).model_dump()
    

class ScheduleRes(BaseModel):
    worktime: WorktimeAsForeign
    schedule: list[WorkdayAsPrimary]

    @staticmethod
    def to_json(
        worktime: Worktime,
        schedule: list[Workday],
        me: User | None
    ):
        return ScheduleRes(
            worktime = WorktimeAsForeign.to_json(worktime),
            schedule = [
                WorkdayAsPrimary.to_json(workday, me)
                for workday in schedule
            ]
        ).model_dump()
    

class FreeSlotAsElement(BaseModel):
    startTime: str
    endTime: str

    def duration(self) -> timedelta:
        format = '%H:%M:%S'
        return calc.str_to_time(self.endTime, format) - calc.str_to_time(self.startTime, format)


class FreeSlotsRes(BaseModel):
    freeSlots: list[FreeSlotAsElement]
    priceList: list[PriceAsPrimary]

    @staticmethod
    def to_json(freeSlots: list[FreeSlotAsElement], workday: Workday):
        return FreeSlotsRes(
            freeSlots = freeSlots,
            priceList = [PriceAsPrimary.to_json(price) for price in workday.doctor.price_list]
        ).model_dump()