from .api import router as doctor_router
from .medical_records import medical_records_router
from .types import MySchedule

doctor_router.include_router(medical_records_router)