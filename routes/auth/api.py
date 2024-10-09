from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import connect_db
from utils.facades import auth, hash, typo
from entities.user import UserQuery, UserAsPrimary
from .types import SignInReq


router = APIRouter()


@router.post('', response_model = UserAsPrimary)
async def sign_in(
    request_data: SignInReq = Body(),
    db: AsyncSession = Depends(connect_db)
):
    user_query = UserQuery(db)
    login = request_data.login.strip()
    password_hash = hash.it(request_data.password)
    
    if typo.is_email(login):
        user = await user_query.get_by_email(login, password_hash)
    elif typo.is_iin(login):
        user = await user_query.get_by_iin(login, password_hash)
    else: raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f'Field "{login}" Not Acceptable For Email or IIN Formats'
    )
        
    return JSONResponse(
        headers = auth.get_auth_headers(user.id),
        content = UserAsPrimary.to_json(user)
    )