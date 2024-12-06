from fastapi import (
    Header,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from entities.user import User, UserQuery, Role
from core.facades.auth import generate_token, authenticate_token


def get_auth_headers(me: User | None) -> dict[str, str] | None:
    return {
        'Auth': f'Bearer { generate_token(me.id) }'
    } if me is not None else None


async def authenticate_me(
    token: str = Header(alias='Auth'),
    db: AsyncSession = Depends(connect_db)
) -> User:
    try:
        me = await UserQuery(db).get_by_id(authenticate_token(token))
    except:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid Token'
        )
    
    if me is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid Token'
        )
    return me


async def authenticate_me_if_token(
    token: str | None = Header(None, alias = 'Auth'),
    db: AsyncSession = Depends(connect_db)
) -> User | None:
    if token is None: return None
    try:
        return await UserQuery(db).get_by_id(authenticate_token(token))
    except: return None


async def authenticate_me_as_doctor(
    token: str = Header(alias='Auth'),
    db: AsyncSession = Depends(connect_db)
) -> User:
    me = await authenticate_me(token, db)
    if me.role_type == Role.DOCTOR and me.as_doctor is not None:
        return me
    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        'This Module Forbidden for You'
    )