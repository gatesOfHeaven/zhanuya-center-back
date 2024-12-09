from .api import manager_router
from .doctors import doctors_router
from .patients import patients_router


manager_router.include_router(doctors_router)
manager_router.include_router(patients_router)