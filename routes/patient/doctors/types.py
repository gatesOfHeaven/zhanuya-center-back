from pydantic import BaseModel

from utils.facades import calc
from entities.user import User
from entities.doctor import Doctor
from entities.category import CategoryAsForeign
from entities.office import OfficeAsForeign
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
    office: OfficeAsForeign

    def to_json(doctor: Doctor):
        return DoctorAsElement(
            id = doctor.id,
            name = doctor.profile.name,
            surname = doctor.profile.surname,
            avatarUrl = doctor.avatar_url,
            age = calc.get_age(doctor.profile.birth_date),
            expInMonthes = calc.get_monthes(doctor.career_started_on),
            category = CategoryAsForeign.to_json(doctor.category),
            office = OfficeAsForeign.to_json(doctor.office)
        ).model_dump()
    

class DoctorAsPage(BaseModel):
    profile: DoctorAsElement
    worktime: WorktimeAsForeign
    schedule: list[WorkdayAsPrimary]

    def to_json(
        doctor: Doctor,
        worktime: Worktime,
        schedule: list[Workday],
        me: User | None
    ):
        return DoctorAsPage(
            profile = DoctorAsElement.to_json(doctor),
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
        return DoctorAsPage(
            worktime = WorktimeAsForeign.to_json(worktime),
            schedule = [
                WorkdayAsPrimary.to_json(workday, me)
                for workday in schedule
            ]
        ).model_dump()