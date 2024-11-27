from pydantic import BaseModel, Field

from entities.medical_record import MedicalRecord, MedicalRecordType


class AddMedicalRecordReq(BaseModel):
    appointment_id: int = Field(gt = 0)
    type: MedicalRecordType
    title: str = Field(min_length = 1, max_length = MedicalRecord._title_max_len)
    content: str = Field(min_length = 5, max_length = MedicalRecord._content_max_len)


class EditMedicalRecordReq(BaseModel):
    type: MedicalRecordType | None = Field(default = None)
    title: str | None = Field(min_length = 1, max_length = MedicalRecord._title_max_len, default = None)
    content: str | None = Field(min_length = 5, max_length = MedicalRecord._content_max_len, default = None)