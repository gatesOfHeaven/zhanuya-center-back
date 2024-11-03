from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from utils import connect_db
from utils.facades import auth, calc
from entities.user import User
from entities.doctor import DoctorQuery, DoctorAsPrimary
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery, CURR_WEEK_NUM
from .types import DoctorAsElement, ScheduleRes, FreeSlotAsElement, FreeSlotsRes


router = APIRouter(tags = ['doctors'])


@router.get('', response_model = DoctorAsElement)
async def search_doctors(
    fullname: str | None = Query(None),
    categories: list[int] | None = Query(None, alias = 'categories[]'),
    min_exp_years: int | None = Query(None),
    offices: list[int] | None = Query(None, alias = 'offices[]'),
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


@router.get('/{id}/{week_num}', response_model = ScheduleRes)
async def doctor_schedule(
    id: int = Path(gt = 0),
    week_num: int = Path(ge = CURR_WEEK_NUM, le = 3),
    me: User | None = Depends(auth.authenticate_me_if_token),
    db: AsyncSession = Depends(connect_db)
):
    doctor = await DoctorQuery(db).get(id)
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = ScheduleRes.to_json(
            worktime = await WorktimeQuery(db).get_actual(),
            schedule = await WorkdayQuery(db).get_schedule(doctor, week_num),
            me = me
        )
    )


@router.get('/{id}/day/{date}', response_model = FreeSlotsRes)
async def free_slots(
    id: int = Path(gt = 0),
    date: str = Path(pattern = r'\d{2}\.\d{2}\.\d{4}'),
    per_hour: int = Query(gt = 0, le = 60, default = 2),
    db: AsyncSession = Depends(connect_db)    
):
    workday = await WorkdayQuery(db).get(
        doctor = await DoctorQuery(db).get(id),
        day = calc.str_to_time(date, '%d.%m.%Y').date()
    )
    next_slots = workday.slots.copy()
    free_slots: list[FreeSlotAsElement] = []
    current_timepoint: datetime = workday.start_datetime()
    increment_interval = timedelta(minutes = 60 / per_hour)

    while current_timepoint < workday.end_datetime():
        lunch = workday.lunch
        is_free = True
        next_timepoint = current_timepoint + increment_interval

        if lunch is None or not lunch.start_datetime() <= current_timepoint < lunch.end_datetime():
            while len(next_slots) > 0 and next_slots[0].start_datetime() <= current_timepoint:
                is_free = False
                past_slot = next_slots.pop(0)
                print(past_slot.start_datetime())

            if is_free: free_slots.append(FreeSlotAsElement(
                startTime = calc.time_to_str(current_timepoint, '%H:%M:%S'),
                endTime = calc.time_to_str(next_timepoint, '%H:%M:%S')
            ))
        current_timepoint = next_timepoint

    return JSONResponse(FreeSlotsRes.to_json(
        freeSlots = free_slots,
        workday = workday
    ))