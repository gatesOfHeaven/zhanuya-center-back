from fastapi import APIRouter, status, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import connect_db
from utils.facades import auth
from entities.user import User
from entities.doctor import DoctorQuery, DoctorAsPrimary
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery, CURR_WEEK_NUM
from entities.appointment_type import AppointmentTypeQuery
from entities.slot import SlotQuery
from .types import DoctorAsElement, Schedule, MakeAppointmentReq


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


@router.get('/{id}', response_model = DoctorAsPrimary)
async def doctor_profile(
    id: int = Path(gt = 0),
    me: User | None = Depends(auth.authenticate_me_if_token),
    db: AsyncSession = Depends(connect_db)
):
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = DoctorAsPrimary.to_json(
            await DoctorQuery(db).get(id)
        )
    )


@router.get('/{id}/{week_num}', response_model = Schedule)
async def doctor_profile(
    id: int = Path(gt = 0),
    week_num: int = Path(ge = CURR_WEEK_NUM, le = 3),
    me: User | None = Depends(auth.authenticate_me_if_token),
    db: AsyncSession = Depends(connect_db)
):
    doctor = await DoctorQuery(db).get(id)
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = Schedule.to_json(
            worktime = await WorktimeQuery(db).get_actual(),
            schedule = await WorkdayQuery(db).get_schedule(doctor, week_num),
            me = me
        )
    )


@router.post('/{id}/{week_num}', response_model = Schedule)
async def make_appointment(
    id: int = Path(gt = 0),
    week_num: int = Path(ge = CURR_WEEK_NUM, le = 3),
    request_data: MakeAppointmentReq = Body(),
    me: User | None = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    workday_query = WorkdayQuery(db)
    doctor = await DoctorQuery(db).get(id)
    await SlotQuery(db).new(
        patient = me,
        workday = await workday_query.get(doctor, request_data.date),
        type = await AppointmentTypeQuery(db).get(request_data.type_id),
        starts_at = request_data.starts_at,
        ends_at = request_data.ends_at
    )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        headers = auth.get_auth_headers(me),
        content = Schedule.to_json(
            worktime = await WorktimeQuery(db).get_actual(),
            schedule = await workday_query.get_schedule(doctor, week_num),
            me = me
        )
    )