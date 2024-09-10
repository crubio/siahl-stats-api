from typing import Union
from fastapi import FastAPI
from .routers import stats
from . import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}