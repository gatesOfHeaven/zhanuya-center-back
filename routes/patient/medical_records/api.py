from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import connect_db
from core.bases import PaginationResponse
from utils.decorators import auth
from entities.user import User
from entities.medical_record import MedicalRecordType, MedicalRecordQuery, MedicalRecordAsElement


router = APIRouter(prefix = '/medical-records', tags = ['medical records'])


@router.get('', response_model = PaginationResponse[MedicalRecordAsElement])
async def my_medical_records(
    record_type: MedicalRecordType | None = Query(default = None),
    offset: int = Query(ge = 0, default = 0),
    limit: int = Query(gt = 0, default = 10),
    me: User = Depends(auth.authenticate_me),
    db: AsyncSession = Depends(connect_db)
):
    medical_records_query = MedicalRecordQuery(db)
    medical_records = await medical_records_query.paginate(
        record_type = record_type,
        offset = offset,
        limit = limit,
        patient = me
    )
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = PaginationResponse.to_json(
            offset = offset,
            limit = limit,
            total = await medical_records_query.total(patient = me, record_type = record_type),
            page = [
                MedicalRecordAsElement.to_json(record)
                for record in medical_records
            ]
        )
    )