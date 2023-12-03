from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import cursor, conn
from routes.jwt import get_current_user, check_is_login
import requests

ayokebali = APIRouter()

@ayokebali.get('/destination')
async def read_data(current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = current_user['data']['token_ayokebali']
    if token:
        ayokebali_url = "https://ayokebalitst.azurewebsites.net"
        destination_url = f"{ayokebali_url}/destination"
        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {token}"
        }

        try:
            # Kirim permintaan GET ke layanan teman
            response = requests.get(destination_url, headers=headers)
            response.raise_for_status()
            destination_data = response.json()
            return {
                "code": 200,
                "messages" : "Get All Destination successfully",
                "data" : destination_data
                }
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to get destination data service: {str(e)}")
    else:
        return {
                "code": 404,
                "messages" : "Failed get All Destination"
                }

@ayokebali.get('/destination/{id}')
async def read_data(id: int,current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = current_user['data']['token_ayokebali']
    if token:
        ayokebali_url = "https://ayokebalitst.azurewebsites.net"
        destination_url = f"{ayokebali_url}/destination/{id}"
        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.get(destination_url, headers=headers)
            response.raise_for_status()
            destination_data = response.json()
            return {
                "code": 200,
                "messages" : "Get Destination successfully",
                "data" : destination_data
                }
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to get destination data service: {str(e)}")
    else:
        return {
                "code": 404,
                "messages" : "Failed get Destination Data"
                }