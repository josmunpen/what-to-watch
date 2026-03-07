from fastapi import FastAPI
from app.routers import recommendations

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to What to Watch API!"}

app.include_router(recommendations.router)