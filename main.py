from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import recommendations
from app.services.tmdb_service import tmdb_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # app is running
    tmdb_service.close()  # close the shared httpx.Client on shutdown


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to What to Watch API!"}


app.include_router(recommendations.router)