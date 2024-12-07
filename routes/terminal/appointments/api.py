from fastapi import APIRouter, HTTPException, status, Path, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint

from core import connect_db
from core.bases import GeneralResponse
from core.facades import memo, mail
from utils.decorators import auth
from entities.terminal import Terminal
from entities.slot import SlotQuery, SlotValidator
from entities.payment import PaymentQuery
from .helpers import key_for
from .types import ConfirmAppointmentReq

router = APIRouter(prefix = '/appointments', tags = ['appointments'])


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
    payment = await PaymentQuery(db).new(
        slot = appointment,
        payment_method = request_data.method,
        provider = terminal,
        commit = False
    )
    if await memo.verify(key_for(appointment), request_data.confirmationCode):
        await db.commit()
    else: raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        'Payment declined. Confirmation Code is Wrong. Please try again'
    )
    return JSONResponse(GeneralResponse.to_json('Payment Success!'))