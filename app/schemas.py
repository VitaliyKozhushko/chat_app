from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
  username: str

class UserCreate(UserBase):
  password: str

class UserResponse(UserBase):
  id: int
  created_at: datetime

  class Config:
    from_attributes = True

class MessageBase(BaseModel):
  content: str

class MessageCreate(MessageBase):
  pass

class MessageResponse(MessageBase):
  id: int
  timestamp: datetime
  sender_id: int
  username: str

  class Config:
    from_attributes = True

class Token(BaseModel):
  access_token: str
  refresh_token: str
  user_id: Optional[int] = None

  class Config:
    from_attributes = True

class RoomBase(BaseModel):
  name: str

class RoomCreate(RoomBase):
  pass

class RoomResponse(RoomBase):
  id: int
  users: Optional[List[UserResponse]] = None

  class Config:
    from_attributes = True