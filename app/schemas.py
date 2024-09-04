from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
  username: str

class UserCreate(UserBase):
  password: str

class UserResponse(UserBase):
  id: int
  created_at: datetime

  class Config:
    orm_mode = True

class MessageBase(BaseModel):
  content: str

class MessageCreate(MessageBase):
  pass

class MessageResponse(MessageBase):
  id: int
  timestamp: datetime
  sender_id: int

  class Config:
    orm_mode = True

class Token(BaseModel):
  access_token: str
  refresh_token: str

  class Config:
    orm_mode = True