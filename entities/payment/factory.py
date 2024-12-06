from random import choice, randint
from datetime import datetime, timedelta

from core.bases import BaseFactory
from entities.slot import Slot
from entities.manager import Manager
from entities.terminal import Terminal
from .entity import Payment
from .values import ProviderType, PaymentMethod


class Factory(BaseFactory):
    async def seed(
        self,
        slots: list[Slot],
        managers: list[Manager],
        terminals: list[Terminal],
        attendance_percentage: int,
        terminal_provider_probability: int
    ):
        fakes: list[Payment] = []
        now = datetime.now()
        for slot in slots:
            if slot.end_datetime() <= now and self.fake.boolean(attendance_percentage):
                terminal, manager = self.random_local_terminal_and_manager(
                    slot = slot,
                    managers = managers,
                    terminals = terminals
                )
                if terminal is None and manager is None: continue
                provider_type = self.provider_type(terminal, manager, terminal_provider_probability)

                slot.payment = Payment(
                    slot = slot,
                    method = choice(list(PaymentMethod)),
                    made_at = slot.start_datetime() + timedelta(seconds = randint(-600, 559)),
                    provider_type = provider_type,
                    provider_id = terminal.id if provider_type == ProviderType.TERMINAL else manager.id
                )
                fakes.append(slot.payment)
            else: slot.payment = None
        await self.flush(slots)
        await self.flush(fakes)
        return fakes
        

    def random_local_terminal_and_manager(
        self,
        slot: Slot,
        managers: list[Manager],
        terminals: list[Terminal]
    ) -> tuple[Terminal | None, Manager | None]:
        building_id = slot.workday.doctor.office.building_id
        local_terminals = [
            terminal for terminal in terminals
            if terminal.building_id == building_id
        ]
        local_managers = [
            manager for manager in managers
            if manager.building_id == building_id
        ]
        return (
            choice(local_terminals) if len(local_terminals) > 0 else None,
            choice(local_managers) if len(local_managers) > 0 else None
        )
    

    def provider_type(
        self,
        terminal: Terminal | None,
        manager: Manager | None,
        terminal_probability: int
    ) -> ProviderType:
        if terminal is None: return ProviderType.MANAGER
        if manager is None or self.fake.boolean(terminal_probability):
            return ProviderType.TERMINAL
        return ProviderType.MANAGER