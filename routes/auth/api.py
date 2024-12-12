from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from core.bases import BaseResponse
from core.facades import hash, typo, calc
from utils.decorators import auth
from entities.user import UserQuery, User
from .types import SignInReq


router = APIRouter(prefix = '/auth', tags = ['for patient', 'for doctor', 'for manager', 'auth'])


# delete
class Temp(BaseResponse):
    id: int
    name: str
    surname: str
    gender: str
    birthDate: str
    age: int
    email: str
    iin: str
    role: str
    buildingId: int | None

    @staticmethod
    def to_json(user: User):
        return Temp(
            id = user.id,
            name = user.name,
            surname = user.surname,
            gender = user.gender.value,
            birthDate = calc.time_to_str(user.birth_date),
            age = calc.get_age(user.birth_date),
            email = user.email,
            iin = user.iin,
            role = user.role_type.value,
            buildingId = None if user.as_manager is None else user.as_manager.building_id
        ).model_dump()


@router.post('', response_model = Temp)
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
        headers = auth.get_auth_headers(user),
        content = Temp.to_json(user)
    )