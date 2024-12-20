from fastapi import APIRouter, HTTPException, status, Path, Body, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint

from core import connect_db
from core.bases import GeneralResponse
from core.facades import memo, mail, calc
from utils.decorators import auth
from entities.terminal import Terminal
from entities.slot import SlotQuery, SlotValidator
from entities.payment import PaymentQuery
from .helpers import key_for, sse_from_appointments
from .types import ConfirmAppointmentReq, SlotAsPrimary

router = APIRouter(prefix = '/appointments', tags = ['appointments'])


@router.get('')
async def to_confirm(
    terminal: Terminal = Depends(auth.authenticate_terminal),
    db: AsyncSession = Depends(connect_db)
):
    return StreamingResponse(
        media_type = 'text/event-stream',
        content = sse_from_appointments(db, terminal)
    )


@router.get('/{id}', response_model = SlotAsPrimary)
async def single_appointment(
    id: int = Path(gt = 0),
    terminal: Terminal = Depends(auth.authenticate_terminal),
    db: AsyncSession = Depends(connect_db)
):
    appointment = await SlotQuery(db).get(id, terminal)
    SlotValidator.validate_pay_ability(appointment)
    return SlotAsPrimary.to_json(appointment)


@router.post('/{id}', response_model = GeneralResponse)
async def send_confirmation_code(
    id: int = Path(gt = 0),
    terminal: Terminal = Depends(auth.authenticate_terminal),
    db: AsyncSession = Depends(connect_db)
):
    appointment = await SlotQuery(db).get(id, terminal)
    SlotValidator.validate_pay_ability(appointment)
    confirmation_code = randint(1000, 9999)
    try:
        await memo.save(key_for(appointment), confirmation_code, 5)
        await mail.send(
            appointment.patient.email,
            'Appointment Confirmation',
            f'Your confirmation code is {confirmation_code}'
        )
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(GeneralResponse.to_json('Confirmation Code was sent to Your Email'))
    


@router.put('/{id}', response_model = GeneralResponse)
async def confirm_appointment(
    id: int = Path(gt = 0),
    request_data: ConfirmAppointmentReq = Body(),
    terminal: Terminal = Depends(auth.authenticate_terminal),
    db: AsyncSession = Depends(connect_db)
):
    appointment = await SlotQuery(db).get(id, terminal)
    SlotValidator.validate_pay_ability(appointment)
    await PaymentQuery(db).new(
        slot = appointment,
        payment_method = request_data.method,
        provider = terminal,
        commit = False
    )
    doctor = appointment.workday.doctor
    if await memo.verify(key_for(appointment), request_data.confirmationCode):
        await db.commit()
        await mail.send(
            reciever_email = doctor.profile.email,
            subject = 'Appointment Confirmed',
            content = f'{appointment.patient.name} {appointment.patient.surname} confirmed an appointment!'
            f'Wait for patient in office {doctor.office.title} at {calc.time_to_str(appointment.starts_at, '%H:%M:%S')}'
        )
    else: raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        'Payment declined. Confirmation Code is Wrong. Please try again'
    )
    return JSONResponse(GeneralResponse.to_json('Payment Success!'))