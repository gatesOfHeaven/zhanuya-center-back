from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING, Optional

from utils.bases import BaseEntity
from .values import PaymentMethod, ProviderType

if TYPE_CHECKING:
    from entities.manager import Manager
    from entities.terminal import Terminal
    from entities.slot import Slot


def get_primaryjoin_condition(entity: str, type: ProviderType) -> str:
    return f'and_(Payment.provider_id == foreign({entity}.id), Payment.provider_type == "{type.name}")'


class Payment(BaseEntity):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key = True)
    slot_id = Column(Integer, ForeignKey('slots.id'), nullable = False)
    method: Mapped[PaymentMethod] = Column(Enum(PaymentMethod), default = PaymentMethod.CACHE, nullable = False)
    made_at = Column(DateTime, nullable = False)
    provider_type: Mapped[ProviderType] = Column(Enum(ProviderType), default = ProviderType.TERMINAL, nullable = False)
    provider_id = Column(Integer, nullable = False)

    slot: Mapped['Slot'] = relationship(back_populates = 'payment')

    terminal: Mapped[Optional['Terminal']] = relationship(
        primaryjoin = get_primaryjoin_condition('Terminal', ProviderType.TERMINAL),
        foreign_keys = [provider_id],
        viewonly = True
    )
    manager: Mapped[Optional['Manager']] = relationship(
        primaryjoin = get_primaryjoin_condition('Manager', ProviderType.MANAGER),
        foreign_keys = [provider_id],
        viewonly = True
    )
    