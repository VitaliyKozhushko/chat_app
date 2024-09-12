from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_session_db
from app.schemas import MessageResponse, RoomResponse, RoomCreate, PrivateMessageResponse
from app.auth import get_current_user
from app.crud import (get_user,
                      get_messages,
                      get_room_by_name,
                      create_new_room,
                      get_room_by_id,
                      get_all_rooms,
                      get_room_messages)
from app.models import User, PrivateMessage

router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get("/chat/{room_id}-{user_id}",response_class=JSONResponse)
async def chat_room(request: Request, room_id: int, db: Session = Depends(get_session_db)):
  print('room_id', room_id)
  room = get_room_messages(db, id=room_id)
  messages = room.messages
  messages_data = [
    {
      "id": message.id,
      "content": message.content,
      "timestamp": message.timestamp.isoformat(),
      "sender": message.sender.username,
      "sender_id": message.sender_id
    }
    for message in messages
  ]
  return JSONResponse(content=messages_data)

@router.get('/rooms', response_model=List[RoomResponse])
def get_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_session_db)):
  rooms = get_all_rooms(db, skip=skip, limit=limit)
  if not rooms:
    return JSONResponse(content={
      'message': 'Созданных комнат нет'
    })
  return rooms

@router.post('/rooms', response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_session_db)):
    existing_room = get_room_by_name(db, name=room.name)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Комната с таким названием уже существует'
        )
    new_room = create_new_room(db, name=room.name)
    return new_room

@router.get('/private_messages/{sender_id}-{recipient_id}', response_model=List[PrivateMessageResponse])
def get_private_messages_between_users(
  sender_id: int,
  recipient_id: int,
  db: Session = Depends(get_session_db),
  current_user: User = Depends(get_current_user)):

  if current_user.id != sender_id and current_user.id != recipient_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещён")

  messages = (db.query(PrivateMessage).options(joinedload(PrivateMessage.sender), joinedload(PrivateMessage.recipient))
              .filter(
                      ((PrivateMessage.sender_id == sender_id) & (PrivateMessage.recipient_id == recipient_id)) |
                      ((PrivateMessage.sender_id == recipient_id) & (PrivateMessage.recipient_id == sender_id)))
              .all())

  response_messages = [
    PrivateMessageResponse(
      id=message.id,
      content=message.content,
      timestamp=message.timestamp,
      sender_id=message.sender_id,
      sender=message.sender.username,
      recipient_id=message.recipient_id,
      recipient=message.recipient.username
    )
    for message in messages
  ]

  return response_messages
