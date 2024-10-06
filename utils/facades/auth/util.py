from fastapi import (
    Header,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import connect_db
from entities.user import User, UserQuery
from .core import generate_token, authenticate_token


def get_auth_headers(id: int) -> dict[str, str]:
    return { 'Auth': f'Bearer { generate_token(id) }' }


async def authenticate_me(
    token: str = Header(alias='Auth'),
    db: AsyncSession = Depends(connect_db)
) -> User:
    me = await UserQuery(db).get_by_id(authenticate_token(token))
    if not me:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid Token'
        )
    return me