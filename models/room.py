from pydantic import BaseModel

class Room(BaseModel):
	id: int
	room_name: str
	price: int
	description: str
	url_video: str