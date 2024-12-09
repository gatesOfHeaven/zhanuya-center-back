from fastapi import APIRouter, status, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from core.bases import GeneralResponse
from core.facades import calc
from utils.decorators import auth, exec
from entities.user import User, UserQuery
from entities.doctor import DoctorQuery
from entities.workday import WorkdayQuery
from entities.price import PriceQuery
from entities.appointment_type import AppointmentTypeQuery
from entities.slot import SlotQuery, MakeAppointmentReq
from .types import PatientAsElement


router = APIRouter(prefix = '/patients', tags = ['patients'])


@router.get('', response_model = list[PatientAsElement])
async def search_patient(
    fullname: str | None = Query(None, max_length = 51),
    iin: str | None = Query(None, pattern = r'^\d+$', max_length = 12),
    db: AsyncSession = Depends(connect_db),
    me: User = Depends(auth.authenticate_me_as_manager)
):
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = [
            PatientAsElement.to_json(patient)
            for patient in await UserQuery(db).search(fullname, iin, 5)
        ]
    )


@router.post('/{id}', response_model = GeneralResponse)
async def assign_appointment(
    id: int = Path(gt = 0),
    request_data: MakeAppointmentReq = Body(),
    db: AsyncSession = Depends(connect_db),
    me: User = Depends(auth.authenticate_me_as_manager)
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
        patient = await UserQuery(db).get_by_id(id),
        workday = workday,
        price = price,
        starts_at = calc.str_to_time(request_data.startsAt, '%H:%M:%S').time(),
        ends_at = calc.str_to_time(request_data.endsAt, '%H:%M:%S').time()
    )
    exec.schedule_appointment_notification(appointment)
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        headers = auth.get_auth_headers(me),
        content = GeneralResponse.to_json('Appointment Created Successfully')
    )