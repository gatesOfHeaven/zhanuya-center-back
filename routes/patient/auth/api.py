from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint

from utils import connect_db
from utils.bases import BaseResponse
from utils.facades import auth, hash, mail, calc
from entities.user import User, UserQuery, UserAsPrimary
from entities.email_verification import EmailVerificationQuery
from .types import SendVerificationReq, VerificationConflictElement, SignUpReq, SignUpRes


router = APIRouter(tags = ['auth'])


verification_responses = {
    status.HTTP_202_ACCEPTED: { 'model': BaseResponse },
    status.HTTP_409_CONFLICT: { 'model': list[VerificationConflictElement] }
}


@router.post('', responses = verification_responses)
async def send_verification_code(
    request_data: SendVerificationReq = Body(),
    db: AsyncSession = Depends(connect_db)
):
    verification_code = randint(1000, 9999)
    email_ok = await EmailVerificationQuery(db).new(
        request_data.email,
        verification_code,
        commit = False
    )
    iin_ok = await UserQuery(db).iin_is_available(request_data.iin)

    if not email_ok or not iin_ok:
        fields: list[VerificationConflictElement] = []
        if not email_ok:
            fields.append(VerificationConflictElement(
                detail = 'Email is Already Taken',
                location = 'email'
            ))
        if not iin_ok:
            fields.append(VerificationConflictElement(
                detail = 'IIN Owner Does NOT Match',
                location = 'iin'
            ))
        return JSONResponse(
            status_code = status.HTTP_409_CONFLICT,
            content = [field.model_dump() for field in fields]
        )

    try:
        await db.commit()
        await mail.send(
            request_data.email,
            'Email Verification',
            f'Your verification code is {verification_code}'
        )
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(
        status_code = 202,
        content = BaseResponse.to_json('Verification Code is sent to your Email')
    )


@router.post('/sign-up', response_model = SignUpRes)
async def sign_up(
    request_data: SignUpReq = Body(),
    db: AsyncSession = Depends(connect_db)
):
    await EmailVerificationQuery(db).verify(
        request_data.email,
        request_data.emailVerificationCode,
        commit = False
    )
    user_query = UserQuery(db)
    user = await user_query.new(
        name = request_data.name,
        surname = request_data.surname,
        email = request_data.email,
        iin = request_data.iin,
        gender = request_data.gender,
        birth_date = calc.str_to_time(request_data.birthDate, '%d-%m-%Y').date(),
        password = request_data.password, # test only
        password_hash = hash.it(request_data.password),
        commit = False
    )
    await user_query.commit()
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = SignUpRes.to_json(user)
    )


@router.get('', response_model = UserAsPrimary)
async def me(me: User = Depends(auth.authenticate_me)):
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = UserAsPrimary.to_json(me)
    )