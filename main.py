from fastapi import FastAPI

import auth
from routes import player
from auth import auth
from db.db import init_database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield

app = FastAPI(
    lifespan= lifespan
)

@app.get("/")
def root():
    return {"message": "Hello world"}

app.include_router(player.router)
app.include_router(player.router2)
app.include_router(auth.router)