from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from routes.jwt import create_access_token, get_current_user
from passlib.context import CryptContext
from db.connection import cursor, conn
import requests

from models.token import Token
from models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = int("60")

auth = APIRouter()

# Token endpoint
@auth.post("/login", response_model=Token)
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result and pwd_context.verify(password, result["password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)

        friend_service_url = "https://ayokebalitst.azurewebsites.net"
        friend_token_url = f"{friend_service_url}/signin"

        friend_token_data = {
            "username": username,
            "password": password
        }

        try:
            # Kirim permintaan POST ke layanan teman dengan format JSON
            response = requests.post(friend_token_url, json=friend_token_data, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            friend_response_data = response.json()
            friend_token = friend_response_data.get("token")
        except requests.RequestException as e:
            print(response.text)
            raise HTTPException(status_code=500, detail=f"Failed to generate token in friend's service: {str(e)}")

        # Save the friend's service token to your database
        query = "UPDATE users SET token_ayokebali = %s WHERE username = %s"
        cursor.execute(query, (friend_token, username))
        conn.commit()

        return {"message": "Login successfully", "access_token": access_token, "token_type": "bearer", "data": {"username": username}}
    
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

    friend_service_url = "https://ayokebalitst.azurewebsites.net"
    friend_register_url = f"{friend_service_url}/register"

    friend_register_data = {
        "username": username,
        "password": password,
    }

    try:
        response = requests.post(friend_register_url, json=friend_register_data)
        response.raise_for_status()
    except requests.RequestException as e:
        # Print the response text for debugging purposes
        print(response.text)
        raise HTTPException(status_code=500, detail=f"Failed to register user in friend's service: {str(e)}")

    return {
        "code": 200,
        "messages": "Register successfully",
        "data": {
            "fullname": fullname,
            "username": username,
        }
    }

# Protected endpoint
@auth.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user