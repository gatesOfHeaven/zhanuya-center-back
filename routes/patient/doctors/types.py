from pydantic import BaseModel, Field

from utils.facades import calc
from entities.user import User
from entities.doctor import Doctor, DoctorAsPrimary
from entities.category import CategoryAsForeign
from entities.room import RoomAsPrimary
from entities.worktime import Worktime, WorktimeAsForeign
from entities.workday import Workday, WorkdayAsPrimary


class DoctorAsElement(BaseModel):
    id: int
    name: str
    surname: str
    avatarUrl: str
    age: int
    expInMonthes: int
    category: CategoryAsForeign
    office: RoomAsPrimary

    def to_json(doctor: Doctor):
        return DoctorAsElement(
            id = doctor.id,
            name = doctor.profile.name,
            surname = doctor.profile.surname,
            avatarUrl = doctor.avatar_url,
            age = calc.get_age(doctor.profile.birth_date),
            expInMonthes = calc.get_monthes(doctor.career_started_on),
            category = CategoryAsForeign.to_json(doctor.category),
            office = RoomAsPrimary.to_json(doctor.office)
        ).model_dump()
    

class DoctorAsPage(BaseModel):
    profile: DoctorAsPrimary
    worktime: WorktimeAsForeign
    schedule: list[WorkdayAsPrimary]

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
    

class Schedule(BaseModel):
    worktime: WorktimeAsForeign
    schedule: list[WorkdayAsPrimary]

    def to_json(
        worktime: Worktime,
        schedule: list[Workday],
        me: User | None
    ):
        return Schedule(
            worktime = WorktimeAsForeign.to_json(worktime),
            schedule = [
                WorkdayAsPrimary.to_json(workday, me)
                for workday in schedule
            ]
        ).model_dump()
    

class MakeAppointmentReq(BaseModel):
    date: str = Field(pattern = r'\d{2}\.\d{2}\.\d{4}')
    type_id: int = Field(gt = 0)
    starts_at: str = Field(pattern = r'\d{2}\:\d{2}\:\d{2}')
    ends_at: str = Field(pattern = r'\d{2}\:\d{2}\:\d{2}')