from sqlalchemy import Column, Integer, String, Enum, Date
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING, Optional

from utils.bases import BaseEntity
from .values import Role, Gender

if TYPE_CHECKING:
    from entities.doctor import Doctor
    from entities.manager import Manager
    from entities.slot import Slot


class User(BaseEntity):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    iin = Column(String(12), unique = True, nullable = False)
    name = Column(String(25), nullable = False)
    surname = Column(String(25), nullable = False)
    role_type: Mapped[Role] = Column(Enum(Role), default = Role.PATIENT, nullable = False)
    gender: Mapped[Gender] = Column(Enum(Gender), nullable=False)
    birth_date = Column(Date, nullable=False)
    password = Column(String(25), nullable = False) # test only
    password_hash = Column(String, nullable = False)

    as_doctor: Mapped[Optional['Doctor']] = relationship(back_populates = 'profile')
    as_manager: Mapped[Optional['Manager']] = relationship(back_populates = 'profile')