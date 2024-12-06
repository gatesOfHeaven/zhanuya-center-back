from core.bases import BaseResponse
from core.facades import calc
from .entity import Payment


class ReceiptAsForeign(BaseResponse):
    id: int
    timestamp: str
    method: str
    provider: str
    amount: int

    @staticmethod
    def to_json(payment: Payment):
        if payment.terminal is not None:
            provider_repr = f'terminal[id={payment.terminal.id}]'
        elif payment.manager is not None:
            profile = payment.manager.profile
            provider_repr = f'manager[id={profile.id}]\n{profile.name} {profile.surname}'
        else: provider_repr = 'not available'

        return ReceiptAsForeign(
            id = payment.id,
            timestamp = calc.time_to_str(payment.made_at, '%d.%m.%Y %H:%M'),
            method = payment.method.value,
            provider = provider_repr,
            amount = payment.slot.price
        ).model_dump()