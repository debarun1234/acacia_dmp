from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    tech_area: str

class UserLogin(BaseModel):
    username: str
    password: str

class DeskCreate(BaseModel):
    desk_id: str
    floor: str
    tech_area: str

class DeskUpdate(BaseModel):
    status: str
