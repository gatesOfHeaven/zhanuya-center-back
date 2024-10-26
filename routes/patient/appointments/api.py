from fastapi import APIRouter, Path, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils import connect_db
from utils.bases import BaseResponse
from utils.facades import auth, calc
from entities.user import User
from entities.appointment_type import AppointmentTypeQuery
from entities.workday import WorkdayQuery
from entities.slot import SlotQuery, SlotAsPrimary, MakeAppointmentReq, MySlotAsElement


router = APIRouter()


@router.get('', response_model = list[MySlotAsElement])
async def my_appointments(
    me: User = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    appointments = await SlotQuery(db).my(me)
    return JSONResponse([
        MySlotAsElement.to_json(appointment, index)
        for index, appointment in enumerate(appointments, 1)
    ])


@router.get('/{id}', response_model = SlotAsPrimary)
async def get_appointment(
    id: int = Path(gt = 0),
    me: User = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    appointment = await SlotQuery(db).get(id, me)
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = SlotAsPrimary.to_json(appointment)
    )


@router.put('/{id}', response_model = SlotAsPrimary)
async def edit_appointment(
    id: int = Path(gt = 0),
    request_data: MakeAppointmentReq = Body(),
    me: User = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    slot_query = SlotQuery(db)
    appointment = await slot_query.get(id, me)
    print(appointment.workday.doctor.profile.surname)
    workday = await WorkdayQuery(db).get(
        doctor = appointment.workday.doctor,
        day = calc.str_to_time(request_data.date, '%d.%m.%Y').date()
    )
    appointment = await slot_query.edit(
        slot = appointment,
        workday = workday,
        appointment_type = await AppointmentTypeQuery(db).get(request_data.type_id),
        start_time = calc.str_to_time(request_data.starts_at, '%H:%M:%S').time(),
        end_time = calc.str_to_time(request_data.ends_at, '%H:%M:%S').time(),
        me = me
    )
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = SlotAsPrimary.to_json(appointment)
    )
    

@router.delete('/{id}', response_model = BaseResponse)
async def cancel_appointment(
    id: int = Path(gt = 0),
    me: User = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    slot_query = SlotQuery(db)
    appointment = await slot_query.get(id, me)
    await slot_query.remove(appointment, me)
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = BaseResponse.to_json('Appointment Canceled')
    )