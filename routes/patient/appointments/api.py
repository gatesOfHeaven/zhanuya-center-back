from fastapi import APIRouter, HTTPException, status, Path, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils import connect_db
from utils.bases import GeneralResponse
from utils.facades import auth, calc, exec
from entities.user import User
from entities.doctor import DoctorQuery
from entities.appointment_type import AppointmentTypeQuery
from entities.price import PriceQuery
from entities.workday import WorkdayQuery
from entities.slot import SlotQuery
from .types import SlotAsPrimary, MySlotAsElement, MakeAppointmentReq


router = APIRouter(tags = ['appointments'])


@router.get('', response_model = list[MySlotAsElement])
async def my_appointments(
    me: User = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    appointments = await SlotQuery(db).my(me)
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = [MySlotAsElement.to_json(appointment) for appointment in appointments]
    )


@router.post('', response_model = GeneralResponse)
async def make_appointment(
    request_data: MakeAppointmentReq = Body(),
    me: User | None = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    doctor = await DoctorQuery(db).get(request_data.doctorId)
    workday = await WorkdayQuery(db).get(
        doctor = doctor,
        day = calc.str_to_time(request_data.date, '%d.%m.%Y').date()
    )
    price = await PriceQuery(db).get(
        doctor = doctor,
        appointment_type = await AppointmentTypeQuery(db).get(request_data.typeId)
    )
    appointment = await SlotQuery(db).new(
        patient = me,
        workday = workday,
        price = price,
        starts_at = calc.str_to_time(request_data.startsAt, '%H:%M:%S').time(),
        ends_at = calc.str_to_time(request_data.endsAt, '%H:%M:%S').time()
    )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        headers = auth.get_auth_headers(me),
        content = GeneralResponse.to_json('Appointment Created Successfully')
    )


@router.get('/{id}', response_model = SlotAsPrimary, tags = ['for doctor'])
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
    doctor = await DoctorQuery(db).get(request_data.doctorId)
    workday = await WorkdayQuery(db).get(
        doctor = doctor,
        day = calc.str_to_time(request_data.date, '%d.%m.%Y').date()
    )
    price = await PriceQuery(db).get(
        doctor = doctor,
        appointment_type = await AppointmentTypeQuery(db).get(request_data.typeId)
    )
    appointment = await slot_query.edit(
        slot = appointment,
        workday = workday,
        price = price,
        start_time = calc.str_to_time(request_data.startsAt, '%H:%M:%S').time(),
        end_time = calc.str_to_time(request_data.endsAt, '%H:%M:%S').time(),
        me = me
    )
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = SlotAsPrimary.to_json(appointment)
    )
    

@router.delete('/{id}', response_model = GeneralResponse)
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
        content = GeneralResponse.to_json('Appointment Canceled')
    )