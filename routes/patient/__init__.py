from .api import patient_router
from .auth import auth_router
from .resources import resources_router
from .doctors import doctors_router
from .appointments import appointments_router
from .medical_records import medical_records_router


patient_router.include_router(auth_router)
patient_router.include_router(resources_router)
patient_router.include_router(doctors_router)
patient_router.include_router(appointments_router)
patient_router.include_router(medical_records_router)