from typing import Union
from fastapi import FastAPI
from .routers import stats
from . import models

app = FastAPI()

app.include_router(stats.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}