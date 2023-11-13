from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from routes.jwt import create_access_token, get_current_user
from passlib.context import CryptContext
from db.connection import cursor, conn

from models.token import Token
from models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = int("60")

auth = APIRouter()

# Token endpoint
@auth.post("/login", response_model=Token)
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    query = ("SELECT * FROM users WHERE username = %s")
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result and pwd_context.verify(password, result["password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"message": "Login successfully", "access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Registration endpoint
@auth.post("/register")
async def register(fullname: str = Form(...), username: str = Form(...), password: str = Form(...), role: str = Form(default="user")):
    # Check sudah ada belum
    query = ("SELECT * FROM users WHERE username = %s")
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    if result:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Username already exist")
    
    hashed_password = pwd_context.hash(password)
    query = "INSERT INTO users (fullname, username, password, role) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (fullname, username, hashed_password, role,))
    conn.commit()
    return {
            "code": 200,
            "messages" : "Register successfully",
            "data" : {
                "fullname" : fullname,
                "username" : username,
            }
    }

# Protected endpoint
@auth.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user