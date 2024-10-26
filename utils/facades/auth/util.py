from fastapi import (
    Header,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from utils import connect_db
from entities.user import User, UserQuery
from .core import generate_token, authenticate_token


def get_auth_headers(me: User | None) -> dict[str, str] | None:
    return {
        'Auth': f'Bearer { generate_token(me.id) }'
    } if me is not None else None


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


async def authenticate_me_if_token(
    token: str | None = Header(None, alias='Auth'),
    db: AsyncSession = Depends(connect_db)
) -> User | None:
    return await authenticate_me(token, db) if token else None