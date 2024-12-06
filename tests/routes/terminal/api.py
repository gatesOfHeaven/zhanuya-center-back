from fastapi import APIRouter, status, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from core.facades import mail
from entities.slot import SlotQuery
router = APIRouter()


@router.post('/appointment/{id}')
async def confirm_appointment(
    id: int = Path(gt = 0),
    db: AsyncSession = Depends(connect_db)
):
    appointment = await SlotQuery(db).get()
    mail.send()