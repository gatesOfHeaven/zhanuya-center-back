from fastapi import APIRouter
from .auth.api import router as auth_router
from .resources import resources_router
from .doctors import doctors_router


patient_router = APIRouter(prefix = '/patient')
patient_router.include_router(auth_router, prefix = '/auth')
patient_router.include_router(resources_router, prefix = '/resources')
patient_router.include_router(doctors_router, prefix = '/doctors')


__all__ = ['patient_router']