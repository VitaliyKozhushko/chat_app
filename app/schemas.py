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
  room_id: int

class MessageResponse(MessageBase):
  id: int
  timestamp: datetime
  sender_id: int
  sender: str

  class Config:
    from_attributes = True

class PrivateMessageCreate(BaseModel):
    recipient_id: int
    content: str


class PrivateMessageResponse(BaseModel):
  id: int
  content: str
  timestamp: datetime
  sender_id: int
  sender: str
  recipient_id: int
  recipient: str

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