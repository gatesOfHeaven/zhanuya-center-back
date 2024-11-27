from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING, Optional

from utils.bases import BaseEntity
from .values import MedicalRecordType

if TYPE_CHECKING:
    from entities.slot import Slot
    from entities.manager import Manager


class MedicalRecord(BaseEntity):
    __tablename__ = 'medical_records'
    _title_max_len = 100
    _content_max_len = 500

    id = Column(Integer, primary_key = True)
    slot_id = Column(Integer, ForeignKey('slots.id'), nullable = False)
    type: Mapped[MedicalRecordType] = Column(Enum(MedicalRecordType), default = MedicalRecordType.TEST, nullable = False)
    added_at = Column(DateTime, nullable = False)
    title = Column(String(_title_max_len), nullable = False)
    content = Column(String(_content_max_len), nullable = False)
    approved_by = Column(Integer, ForeignKey('managers.id'), nullable = True)

    slot: Mapped['Slot'] = relationship(back_populates = 'records')
    approved_manager: Mapped[Optional['Manager']] = relationship()