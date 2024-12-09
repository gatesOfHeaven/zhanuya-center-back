from fastapi import (
    Header,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from entities.user import User, UserQuery, Role
from entities.manager import Manager
from entities.terminal import Terminal, TerminalQuery
from core.facades.auth import generate_token, authenticate_token


user_auth_header_key = 'Auth'
terminal_auth_header_key = 'Terminal-Auth'
manager_key = 'managerId'
terminal_key = 'terminalId'


def get_auth_headers(me: User | None) -> dict[str, str] | None:
    return {
        user_auth_header_key: f'Bearer { generate_token(me.id) }'
    } if me is not None else None


async def authenticate_me(
    token: str = Header(alias=user_auth_header_key),
    db: AsyncSession = Depends(connect_db)
) -> User:
    try: return await UserQuery(db).get_by_id(int(authenticate_token(token)))
    except: raise HTTPException(status.HTTP_401_UNAUTHORIZED)


async def authenticate_me_if_token(
    token: str | None = Header(None, alias = user_auth_header_key),
    db: AsyncSession = Depends(connect_db)
) -> User | None:
    if token is None: return None
    try: return await UserQuery(db).get_by_id(int(authenticate_token(token)))
    except: return None


async def authenticate_me_as_doctor(
    token: str = Header(alias = user_auth_header_key),
    db: AsyncSession = Depends(connect_db)
) -> User:
    me = await authenticate_me(token, db)
    if me.role_type == Role.DOCTOR and me.as_doctor is not None:
        return me
    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        'This Module Forbidden for You'
    )


async def authenticate_me_as_manager(
    token: str = Header(alias = user_auth_header_key),
    db: AsyncSession = Depends(connect_db)
) -> User:
    me = await authenticate_me(token, db)
    if me.role_type == Role.MANAGER and me.as_manager is not None:
        return me
    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        'This Module Forbidden for You'
    )


def get_terminal_auth_headers(manager: User | Manager, terminal: Terminal):
    return { terminal_auth_header_key: generate_token(f'{manager.id}-{terminal.id}') }


async def authenticate_terminal(
    token: str = Header(alias = terminal_auth_header_key),
    db: AsyncSession = Depends(connect_db)
) -> Terminal:
    try:
        payload: str = authenticate_token(token)
        [manager_id, terminal_id] = map(int, payload.split('-'))
        manager = await UserQuery(db).get_by_id(manager_id)
    except: raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if manager.as_manager is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return await TerminalQuery(db).get(terminal_id, manager.as_manager)