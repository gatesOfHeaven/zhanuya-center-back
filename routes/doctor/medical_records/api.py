from fastapi import APIRouter, Path, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils import connect_db
from utils.bases import GeneralResponse
from utils.facades import auth
from entities.user import User
from entities.slot import SlotQuery, SlotValidator
from entities.medical_record import MedicalRecordQuery
from .types import AddMedicalRecordReq, EditMedicalRecordReq


router = APIRouter(tags = ['medical records'])


@router.post('', response_model = GeneralResponse)
async def add_medical_record(
    request_data: AddMedicalRecordReq = Body(),
    me: User = Depends(auth.authenticate_me_as_doctor),
    db: AsyncSession = Depends(connect_db)
):
    appointment = await SlotQuery(db).get(request_data.appointment_id, me)
    SlotValidator.validate_medical_history_access(appointment)
    await MedicalRecordQuery(db).new(
        slot = appointment,
        record_type = request_data.type,
        title = request_data.title,
        content = request_data.content
    )
    return GeneralResponse.to_json('Successfuly Created')


@router.put('/{id}', response_model = GeneralResponse)
async def edit_medical_record(
    id: int = Path(gt = 0),
    request_data: EditMedicalRecordReq = Body(),
    me: User = Depends(auth.authenticate_me_as_doctor),
    db: AsyncSession = Depends(connect_db)
):
    medical_record = await MedicalRecordQuery(db).get(id, me)
    SlotValidator.validate_medical_history_access(medical_record.slot)
    await MedicalRecordQuery(db).edit(
        medical_record = medical_record,
        record_type = request_data.type,
        title = request_data.title,
        content = request_data.content
    )
    return GeneralResponse.to_json('Successfuly Edited')


@router.delete('/{id}', response_model = GeneralResponse)
async def delete_medical_record(
    id: int = Path(gt = 0),
    me: User = Depends(auth.authenticate_me_as_doctor),
    db: AsyncSession = Depends(connect_db)
):
    medical_record = await MedicalRecordQuery(db).get(id, me)
    SlotValidator.validate_medical_history_access(medical_record.slot)
    await MedicalRecordQuery(db).delete(medical_record, me)
    return GeneralResponse.to_json('Successfuly Deleted')