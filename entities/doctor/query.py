from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload

from utils.bases import BaseQuery
from utils.facades import calc
from entities.user import User
from entities.category import Category
from entities.office import Office
from .entity import Doctor


class Query(BaseQuery):
    async def all(self) -> list[Doctor]:
        query = select(Doctor).options(joinedload(Doctor.profile))
        return (await self.db.execute(query)).scalars().all()


    async def search_and_filter(
        self,
        fullname: str | None = None,
        categories: list[str] | None = None,
        min_exp_years: int | None = None,
        max_exp_years: int | None = None,
        offices: list[str] | None = None,
        sort_by: str = 'name',
        asc_order: bool = True
    ) -> list[Doctor]:
        query = select(Doctor).options(
            joinedload(Doctor.profile),
            joinedload(Doctor.category),
            joinedload(Doctor.office)
        )

        if fullname is not None: query = (query
            .join(User).where(or_(
                User.name.ilike(f"{fullname}%"),
                User.surname.ilike(f"{fullname}%")
            ))
        )

        if categories is not None: query = (query
            .join(Category).where(Category.title.in_(categories))
        )

        if offices is not None: query = (query
            .join(Office).where(Office.address.in_(offices))
        )
        
        if min_exp_years is not None: query = query.where(
            calc.get_monthes(Doctor.career_started_on) > 12 * min_exp_years
        )
        
        if max_exp_years is not None: query = query.where(
            calc.get_monthes(Doctor.career_started_on) < 12 * max_exp_years
        )

        if sort_by == 'name':
            query = query.join(User).order_by(User.name.asc() if asc_order else User.name.desc())
        elif sort_by == 'surname':
            query = query.join(User).order_by(User.surname.asc() if asc_order else User.surname.desc())
        elif sort_by == 'category':
            query = query.join(Category).order_by(Category.title.asc() if asc_order else Category.title.desc())
        elif sort_by == 'experience':
            query = query.join(Office).order_by(Office.address.asc() if asc_order else Office.address.desc())
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid sort_by field: {sort_by}")
        return (await self.db.execute(query)).scalars().all()