from fastapi import APIRouter


patient_router = APIRouter(prefix = '/patient', tags = ['for patient'])