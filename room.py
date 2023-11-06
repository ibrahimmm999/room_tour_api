from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel


class Item(BaseModel):
	id: int
	room_name: str
	price: int
	description: str
	url_video: str

json_filename="room.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

app = FastAPI()

@app.get('/room')
async def read_all_room():
	return data['room']


@app.get('/room/{item_id}')
async def read_room(item_id: int):
	for room_item in data['room']:
		print(room_item)
		if room_item['id'] == item_id:
			return room_item
	raise HTTPException(
		status_code=404, detail='room not found'
	)

@app.post('/room')
async def add_room(item: Item):
	item_dict = item.dict()
	item_found = False
	for room_item in data['room']:
		if room_item['id'] == item_dict['id']:
			item_found = True
			return "room ID "+str(item_dict['id'])+" exists."
	
	if not item_found:
		data['room'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@app.put('/room')
async def update_room(item: Item):
	item_dict = item.dict()
	item_found = False
	for room_idx, room_item in enumerate(data['room']):
		if room_item['id'] == item_dict['id']:
			item_found = True
			data['room'][room_idx]=item_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "room ID not found."
	raise HTTPException(
		status_code=404, detail='item not found'
	)

@app.delete('/room/{item_id}')
async def delete_room(item_id: int):

	item_found = False
	for room_idx, room_item in enumerate(data['room']):
		if room_item['id'] == item_id:
			item_found = True
			data['room'].pop(room_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "room ID not found."
	raise HTTPException(
		status_code=404, detail='item not found'
	)
