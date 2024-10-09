from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped
from typing import TYPE_CHECKING

from utils.db import BaseEntity

if TYPE_CHECKING:
    from entities.role import Role
    from entities.slot import Slot


class User(BaseEntity):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    iin = Column(String(12), unique = True, nullable = False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    name = Column(String(25), nullable = False)
    surname = Column(String(25), nullable = False)
    gender = Column(String(6), nullable=False)
    birth_date = Column(Date, nullable=False)
    password = Column(String(25), nullable = False)
    password_hash = Column(String, nullable = False)

    role: Mapped['Role'] = relationship(back_populates = 'users')
    slots: Mapped[list['Slot'] | None] = relationship(back_populates = 'patient')