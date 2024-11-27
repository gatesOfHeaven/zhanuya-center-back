from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from utils import lifespan
from utils.middlewares import DecodeBracketsMiddleware
from routes.auth import auth_router
from routes.patient import patient_router
from routes.doctor import doctor_router


load_dotenv()


app = FastAPI(
    title = 'Happy Patient Medical Center😷',
    lifespan = lifespan,
    default_response_class = JSONResponse,
    redirect_slashes = False
)

app.include_router(auth_router, prefix = '/auth')
app.include_router(patient_router)
app.include_router(doctor_router)

app.add_middleware(DecodeBracketsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
    expose_headers = ['*']
)


if __name__ == '__main__':
    from uvicorn import run
    run(
        'main:app',
        host = '0.0.0.0',
        reload = True,
        port = 2222
    )