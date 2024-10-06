from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint

from utils.db import connect_db
from utils.facades import auth, hash, mail
from entities.user import User, UserQuery, UserAsPrimary
from entities.email_verification import EmailVerificationQuery
from .types import SendVerificationReq, SignUpReq, SignUpRes


router = APIRouter()


@router.post('/', response_model = None)
async def send_verification_code(
    request_data: SendVerificationReq = Body(),
    db: AsyncSession = Depends(connect_db)
):
    verification_code = randint(1000, 9999)
    await EmailVerificationQuery(db).new(
        request_data.email,
        verification_code,
        commit = False
    )
    try:
        await db.commit()
        mail.send_verification_code(request_data.email, verification_code)
    except:
        await db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(status_code = 202, content = {})


@router.post('/sign-up', response_model = SignUpRes)
async def sign_up(
    request_data: SignUpReq = Body(),
    db: AsyncSession = Depends(connect_db)
):
    await EmailVerificationQuery(db).verify(
        request_data.email,
        request_data.emailVerificationCode
    )
    user = await UserQuery(db).new(
        name = request_data.name,
        surname = request_data.surname,
        email = request_data.email,
        gender = request_data.gender,
        birth_date = request_data.birthDate,
        password_hash = hash.it(request_data.password)
    )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = SignUpRes.to_json(user)
    )


@router.get('/me', response_model = UserAsPrimary)
async def me(me: User = Depends(auth.authenticate_me)):
    return JSONResponse(
        headers = auth.get_auth_headers(me.id),
        content = UserAsPrimary.resource(me)
    )