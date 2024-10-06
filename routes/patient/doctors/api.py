from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import connect_db
from entities.doctor import DoctorQuery
from .types import DoctorAsElement


router = APIRouter()


@router.get('', response_model = DoctorAsElement)
async def search_doctors(
    fullname: str | None = Query(None),
    categories: list[str] | None = Query(None),
    min_exp_years: int | None = Query(None, alias = 'min-exp-years'),
    offices: list[str] | None = Query(None),
    sort_by: str = Query('name', alias = 'sort-by'),
    asc_order: bool = Query(True, alias = 'asc-order'),
    db: AsyncSession = Depends(connect_db)
):
    doctors = await DoctorQuery(db).search_and_filter(
        fullname = fullname,
        categories = categories,
        min_exp_years = min_exp_years,
        offices = offices,
        sort_by = sort_by,
        asc_order = asc_order
    )
    return JSONResponse([
        DoctorAsElement.to_json(doctor)
        for doctor in doctors
    ])