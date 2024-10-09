from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db import connect_db
from entities.doctor import DoctorQuery
from entities.category import CategoryQuery
from entities.building import BuildingQuery
from .types import ResourcesRes


router = APIRouter()


@router.get('', response_model = ResourcesRes)
async def get_resources(
    doctors: bool = Query(False),
    categories: bool = Query(False),
    offices: bool = Query(False),
    db: AsyncSession = Depends(connect_db)
):
    return JSONResponse(ResourcesRes.to_json(
        doctors = await DoctorQuery(db).all() if doctors else [],
        categories = await CategoryQuery(db).all() if categories else [],
        offices = await BuildingQuery(db).all() if offices else []
    ))