from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from core.middlewares import DecodeBracketsMiddleware
from utils.lifespan import lifespan
from routes.auth import auth_router
from routes.patient import patient_router
from routes.doctor import doctor_router
from routes.manager import manager_router
from routes.terminal import terminal_router


load_dotenv()


app = FastAPI(
    title = 'Happy Patient Medical Center😷',
    lifespan = lifespan,
    default_response_class = JSONResponse,
    redirect_slashes = False
)

app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(manager_router)
app.include_router(doctor_router)
app.include_router(manager_router)
app.include_router(terminal_router)

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
    # docker run -d --name asyncredis -p 6379:6379 redis:latest
    # docker start asyncredis
    # docker stop asyncredis
    # docker stop $(docker ps -q)