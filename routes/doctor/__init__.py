from .api import router as doctor_router
from .medical_records import medical_records_router


doctor_router.include_router(medical_records_router, prefix = '/medical-records')