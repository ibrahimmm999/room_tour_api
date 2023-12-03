from pydantic import BaseModel

class User(BaseModel):
    fullname: str
    username: str
    password: str
    role: str
    token_ayokebali: str