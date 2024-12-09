from datetime import datetime

from core.bases import BaseQuery
from entities.slot import Slot
from entities.manager import Manager
from entities.terminal import Terminal
from .entity import Payment
from .values import PaymentMethod, ProviderType


class Query(BaseQuery):
    async def new(
        self,
        slot: Slot,
        payment_method: PaymentMethod,
        provider: Manager | Terminal,
        commit: bool = True
    ) -> Payment:
        payment = Payment(
            slot = slot,
            method = payment_method,
            provider_type = ProviderType.MANAGER if isinstance(provider, Manager) else ProviderType.TERMINAL,
            provider_id = provider.id,
            made_at = datetime.now()
        )
        self.db.add(payment)
        if commit: await self.commit()
        return payment