from fastapi import FastAPI

from routes.room import room
from routes.auth import auth
from routes.ayokebali import ayokebali
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Setelan CORS untuk menerima permintaan dari semua domain
origins = ["*"]

# Tambahkan middleware CORS ke aplikasi
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(room)
app.include_router(auth)
app.include_router(ayokebali)