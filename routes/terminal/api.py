from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from core.bases import GeneralResponse
from core.facades import hash, typo
from utils.decorators import auth
from entities.user import UserQuery
from entities.terminal import Terminal, TerminalQuery
from .types import AuthAsManagerReq

router = APIRouter(prefix = '/terminal', tags = ['for terminal'])


@router.post('/auth', response_model = GeneralResponse, tags = ['auth'])
async def turn_on_terminal(
    request_data: AuthAsManagerReq = Body(),
    db: AsyncSession = Depends(connect_db)
):
    user_query = UserQuery(db)
    login = request_data.login.strip()
    password_hash = hash.it(request_data.password)
    
    if typo.is_email(login):
        manager = await user_query.get_by_email(login, password_hash)
    elif typo.is_iin(login):
        manager = await user_query.get_by_iin(login, password_hash)
    else: raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f'Field "{login}" Not Acceptable For Email or IIN Formats'
    )

    terminal = await TerminalQuery(db).get(request_data.terminalId, manager.as_manager)
    return JSONResponse(
        headers = auth.get_terminal_auth_headers(manager, terminal),
        content = GeneralResponse.to_json(f'Welcome, {manager.name} {manager.surname}!')
    )


@router.get('/me')
async def me(terminal: Terminal = Depends(auth.authenticate_terminal)):
    return terminal.id