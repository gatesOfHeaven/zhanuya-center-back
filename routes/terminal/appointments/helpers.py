from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import sleep
from json import dumps

from entities.slot import Slot, SlotQuery
from entities.terminal import Terminal
from .types import AppointmentAsElement, AppointmentsToManage


def key_for(appointment: Slot) -> str:
    return f'appointment:{appointment.id}'


async def sse_from_appointments(db: AsyncSession, terminal: Terminal):
    client_side_db: list[Slot] = []
    while True:
        try:
            appointments_to_confirm = await SlotQuery(db).to_confirm(terminal)
            yield dumps(AppointmentsToManage.to_json(
                appointments_to_add = [
                    AppointmentAsElement.to_json(appointment) for appointment in appointments_to_confirm
                    if appointment not in client_side_db
                ],
                appointments_to_delete = [
                    appointment.id for appointment in client_side_db
                    if appointment not in appointments_to_confirm
                ]
            ))
            client_side_db = appointments_to_confirm
            await sleep(10)
        except Exception as e:
            print(str(e))
            break