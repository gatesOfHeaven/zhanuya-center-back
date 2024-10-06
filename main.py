from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.db import lifespan
from routes.auth import auth_router
from routes.patient import patient_router


app = FastAPI(
    title = 'Zhanuya Medical Center😷',
    lifespan = lifespan
)

app.include_router(auth_router, prefix = '/auth')
app.include_router(patient_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = ['*'],
    allow_headers = ['*'],
    allow_methods = ['*']
)


if __name__ == '__main__':
    from uvicorn import run
    run('main:app', host = '0.0.0.0', port = 2222, reload = True)