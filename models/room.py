from pydantic import BaseModel

class Room(BaseModel):
	id: int
	name: str
	price: int
	description: str
	url_video: str
	user: int