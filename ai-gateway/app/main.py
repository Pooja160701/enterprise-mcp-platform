from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.database import engine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.API_VERSION,
        "status": "running",
    }


@app.on_event("startup")
def startup():
    with engine.connect():
        print("Connected to PostgreSQL")