from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import connect_db
from utils.facades import auth
from entities.user import User
from entities.doctor import DoctorQuery
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery
from .types import DoctorAsElement, DoctorAsPage, Schedule


router = APIRouter()


@router.get('', response_model = DoctorAsElement)
async def search_doctors(
    fullname: str | None = Query(None),
    categories: list[int] | None = Query(None),
    min_exp_years: int | None = Query(None),
    offices: list[int] | None = Query(None),
    sort_by: str = Query('name'),
    asc_order: bool = Query(True),
    db: AsyncSession = Depends(connect_db)
):
    doctors = await DoctorQuery(db).search_and_filter(
        fullname = fullname,
        categories = categories,
        min_exp_years = min_exp_years,
        offices = offices,
        sort_by = sort_by,
        asc_order = asc_order
    )
    return JSONResponse([
        DoctorAsElement.to_json(doctor)
        for doctor in doctors
    ])


@router.get('/{id}', response_model = DoctorAsPage)
async def doctor_profile(
    id: int = Path(gt = 0),
    week: int = Query(0, ge = 0, le = 3),
    db: AsyncSession = Depends(connect_db),
    me: User | None = Depends(auth.authenticate_me_if_token)
):
    doctor = await DoctorQuery(db).get(id)
    return JSONResponse(
        content = DoctorAsPage.to_json(
            doctor = doctor,
            worktime = await WorktimeQuery(db).get_actual(),
            schedule = await WorkdayQuery(db).get_schedule(doctor, week),
            me = me
        )
    )


@router.get('/{id}/{week_num}', response_model = Schedule)
async def doctor_profile(
    id: int = Path(gt = 0),
    week_num: int = Path(ge = 0, le = 3),
    db: AsyncSession = Depends(connect_db),
    me: User | None = Depends(auth.authenticate_me_if_token)
):
    doctor = await DoctorQuery(db).get(id)
    return JSONResponse(
        content = Schedule.to_json(
            worktime = await WorktimeQuery(db).get_actual(),
            schedule = await WorkdayQuery(db).get_schedule(doctor, week_num),
            me = me
        )
    )