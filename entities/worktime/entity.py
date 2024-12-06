from sqlalchemy import Column, Integer, Date

from core.bases import BaseEntity


class Worktime(BaseEntity):
    __tablename__ = 'worktimes'

    start_date = Column(Date, primary_key = True)
    end_date = Column(Date, nullable = True)
    starts_at = Column(Integer, nullable = False)
    ends_at = Column(Integer, nullable = False)