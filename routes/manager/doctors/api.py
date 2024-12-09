from fastapi import APIRouter, status, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from utils.decorators import auth
from entities.user import User
from entities.doctor import DoctorQuery
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery, CURR_WEEK_NUM
from .types import ScheduleRes


router = APIRouter(prefix = '/doctors', tags = ['doctors'])


@router.get('/{id}/{week_num}', response_model = list[ScheduleRes])
async def doctor_schedule(
    id: int = Path(gt = 0),
    week_num: int = Path(ge = CURR_WEEK_NUM, le = 3),
    me: User | None = Depends(auth.authenticate_me_as_manager),
    db: AsyncSession = Depends(connect_db)
):
    doctor = await DoctorQuery(db).get(id)
    workdays = await WorkdayQuery(db).get_schedule(doctor, week_num)
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = ScheduleRes.to_json(
            worktime = await WorktimeQuery(db).get(workdays[0].date) if workdays else None,
            schedule = workdays,
            show_patients = me.as_manager.building == doctor.office.building
        )
    )