from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import cursor, conn
from routes.jwt import check_is_admin, check_is_login
from models.room import Room

room = APIRouter()

@room.get('/room')
async def read_data(check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    query = "SELECT * FROM rooms;"
    cursor.execute(query)
    data = cursor.fetchall()
    return {
        "code": 200,
        "messages" : "Get All Room successfully",
        "data" : data
    }

@room.get('/room/{id}')
async def read_data(id: int, check: Annotated[bool, Depends(check_is_login)]):
    if not check:
        return
    select_query = "SELECT * FROM rooms WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data room id {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get room successfully",
        "data" : data
    }

@room.post('/room')
async def write_data(room: Room, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    room_json = room.model_dump()
    query = "INSERT INTO rooms(name, price, description, url_video) VALUES(%s, %s, %s, %s);"
    cursor.execute(query, (room_json["name"], room_json["price"], room_json["description"], room_json["url_video"]))
    conn.commit()

    select_query = "SELECT * FROM rooms WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_room = cursor.fetchone()

    return {
        "code": 200,
        "messages" : "Add room successfully",
        "data" : new_room
    }
    
@room.put('/room/{id}')
async def update_data(room: Room, id:int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    room_json = room.model_dump()
    select_query = "SELECT * FROM rooms WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data room id {id} Not Found")
    
    query = "UPDATE rooms SET name = %s, price = %s, description = %s, url_video = %s WHERE rooms.id = %s;"
    cursor.execute(query, (room_json["name"],room_json["price"],room_json["description"],room_json["url_video"], id,))
    conn.commit()

    select_query = "SELECT * FROM rooms WHERE rooms.id = %s;"
    cursor.execute(select_query, (id,))
    new_room = cursor.fetchone()
    
    return {
        "code": 200,
        "messages" : "Update Brand successfully",
        "data" : new_room
    }

@room.delete('/room/{id}')
async def delete_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM rooms WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data room id {id} Not Found")
    
    query = "DELETE FROM rooms WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    return {
        "code": 200,
        "messages" : "Delete room successfully",
    }