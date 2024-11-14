from fastapi import APIRouter
from .auth.api import router as auth_router
from .resources import resources_router
from .doctors import doctors_router
from .appointments import appointments_router
from .medical_records import medical_records_router


patient_router = APIRouter(prefix = '/patient', tags = ['for patient'])
patient_router.include_router(auth_router, prefix = '/auth')
patient_router.include_router(resources_router, prefix = '/resources')
patient_router.include_router(doctors_router, prefix = '/doctors')
patient_router.include_router(appointments_router, prefix = '/appointments')
patient_router.include_router(medical_records_router, prefix = '/medical-records')


__all__ = ['patient_router']