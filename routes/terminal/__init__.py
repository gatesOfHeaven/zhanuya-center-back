from .api import router as terminal_router
from .appointments import appointments_router


terminal_router.include_router(appointments_router)