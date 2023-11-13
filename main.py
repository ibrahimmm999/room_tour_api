from fastapi import FastAPI

from routes.room import room
from routes.auth import auth

app = FastAPI()

app.include_router(room)
app.include_router(auth)