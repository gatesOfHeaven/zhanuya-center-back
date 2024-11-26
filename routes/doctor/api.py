from fastapi import APIRouter, status, HTTPException, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from utils import connect_db
from utils.bases import PaginationResponse
from utils.facades import auth
from entities.user import User
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery
from entities.user import UserQuery
from entities.slot import SlotQuery, SlotValidator
from entities.medical_record import MedicalRecordQuery, MedicalRecordType, MedicalRecordAsElement
from .types import MySchedule, PatientAsPrimary


router = APIRouter(prefix = '/doctor', tags = ['for doctor'])


@router.get('/schedule/{week}', response_model = MySchedule)
async def my_schedule(
    week: int = Path(le = 3),
    me: User = Depends(auth.authenticate_me_as_doctor),
    db: AsyncSession = Depends(connect_db)
):
    workdays = await WorkdayQuery(db).get_schedule(me.as_doctor, week)
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = MySchedule.to_json(
            worktime = await WorktimeQuery(db).get(workdays[0].date) if workdays else None,
            schedule = workdays
        )
    )


@router.get('/appointments/{id}/patient', response_model = PatientAsPrimary)
async def patient_profile(
    id: int = Path(gt = 0),
    me: User = Depends(auth.authenticate_me_as_doctor),
    db: AsyncSession = Depends(connect_db)
):
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = PatientAsPrimary.to_json((await SlotQuery(db).get(id, me)).patient)
    )


@router.get('/appointments/{id}/patient/medical-records', response_model = PaginationResponse[MedicalRecordAsElement])
async def patient_medical_history(
    id: int = Path(gt = 0),
    record_type: MedicalRecordType | None = Query(default = None),
    offset: int = Query(ge = 0, default = 0),
    limit: int = Query(gt = 0, default = 10),
    me: User = Depends(auth.authenticate_me_as_doctor),
    db: AsyncSession = Depends(connect_db)
):
    appointment = await SlotQuery(db).get(id, me)
    SlotValidator.validate_medical_history_access(appointment)
    medical_record_query = MedicalRecordQuery(db)
    
    return JSONResponse(
        headers = auth.get_auth_headers(me),
        content = PaginationResponse.to_json(
            offset = offset,
            limit = limit,
            total = await medical_record_query.total(appointment.patient,record_type),
            page = [
                MedicalRecordAsElement.to_json(record) for record in await medical_record_query.paginate(
                    patient = appointment.patient,
                    record_type = record_type,
                    offset = offset,
                    limit = limit
                )
            ]
        )
    )