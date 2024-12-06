from fastapi import HTTPException, status
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.bases import BaseQuery
from entities.user import User
from entities.category import Category
from entities.price import Price
from entities.building import Building
from entities.room import Room
from .entity import Doctor


class Query(BaseQuery):    
    async def get(self, id: int) -> Doctor:
        query = select(Doctor).options(
            joinedload(Doctor.profile),
            joinedload(Doctor.category),
            joinedload(Doctor.price_list).joinedload(Price.appointment_type),
            joinedload(Doctor.office).joinedload(Room.building),
            joinedload(Doctor.experience),
            joinedload(Doctor.education)
        ).where(Doctor.id == id)
        doctor = (await self.db.execute(query)).unique().scalar_one_or_none()
        if doctor is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                'Such Doctor Not Found'
            )
        return doctor


    async def all(self) -> list[Doctor]:
        query = select(Doctor).options(joinedload(Doctor.profile))
        return await self.fetch_all(query)


    async def search_and_filter(
        self,
        fullname: str | None = None,
        categories: list[int] | None = None,
        min_exp_years: int | None = None,
        offices: list[int] | None = None,
        sort_by: str = 'name',
        asc_order: bool = True
    ) -> list[Doctor]:
        query = select(Doctor).options(
            joinedload(Doctor.profile),
            joinedload(Doctor.category),
            joinedload(Doctor.office).joinedload(Room.building),
            joinedload(Doctor.price_list).joinedload(Price.appointment_type)
        ).join(User).join(Category).join(Room).join(Building)

        if fullname is not None:
            fullname = fullname.strip()
            names = fullname.split(' ')
            if len(names) == 1: query = query.where(or_(
                User.name.ilike(f'{fullname}%'),
                User.surname.ilike(f'{fullname}%')
            ))
            elif len(names) > 1: query = query.where(or_(
                and_(User.name.ilike(f'{names[0]}%'), User.surname.ilike(f'{names[1]}%')),
                and_(User.name.ilike(f'{names[1]}%'), User.surname.ilike(f'{names[0]}%'))
            ))
                

        if categories is not None:
            query = query.where(Doctor.category_id.in_(categories))

        if offices is not None:
            query = query.where(Room.building_id.in_(offices))
        
        if min_exp_years is not None:
            query_years = 12 * (func.extract('year', func.current_date()) - func.extract('year', Doctor.career_started_on))
            query_monthes = func.extract('month', func.current_date()) - func.extract('month', Doctor.career_started_on)
            query = query.where((query_years + query_monthes) > 12 * min_exp_years)

        if sort_by == 'name':
            query = query.order_by(User.name.asc() if asc_order else User.name.desc())
        elif sort_by == 'surname':
            query = query.order_by(User.surname.asc() if asc_order else User.surname.desc())
        elif sort_by == 'category':
            query = query.order_by(Category.title.asc() if asc_order else Category.title.desc())
        elif sort_by == 'experience': query = query.order_by(
            Doctor.career_started_on.desc() if asc_order else Doctor.career_started_on.asc()
        )
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid sort_by field: {sort_by}')
        return await self.fetch_all(query)