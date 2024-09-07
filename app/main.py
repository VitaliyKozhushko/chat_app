from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
from socketio import ASGIApp
from .sockets import sio
from .routers import auth, chat, users
from .database import create_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    logger.info('Application startup complete.')
    yield
    logger.info('Application shutdown initiated.')

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

socketio_app = ASGIApp(sio, other_asgi_app=app)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(users.router)

app.mount('/templates', StaticFiles(directory='templates'), name='templates')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
