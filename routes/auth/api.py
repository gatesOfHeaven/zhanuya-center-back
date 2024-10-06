from fastapi import APIRouter, status, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import connect_db
from utils.facades import auth, hash
from entities.user import UserQuery, UserAsPrimary
from .types import SignInReq


router = APIRouter()


@router.post('', response_model = UserAsPrimary)
async def sign_in(
    request_data: SignInReq = Body(),
    db: AsyncSession = Depends(connect_db)
):
    user = await UserQuery(db).get(
        email = request_data.email,
        password_hash = hash.it(request_data.password)
    )
    return JSONResponse(
        headers = auth.get_auth_headers(user.id),
        content = UserAsPrimary.to_json(user)
    )