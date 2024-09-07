from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app.database import get_session_db
from app.schemas import MessageResponse, RoomResponse, RoomCreate
from app.auth import get_current_user
from app.crud import (get_user,
                      get_messages,
                      get_room_by_name,
                      create_new_room,
                      get_room_by_id,
                      get_all_rooms,
                      get_room_messages)

router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get("/chat/{room_id}-{user_id}", response_class=HTMLResponse)
async def chat_room(request: Request, room_id: int, db: Session = Depends(get_session_db)):
  room = get_room_messages(db, id=room_id)
  messages = room.messages
  messages_data = [
    {
      "id": message.id,
      "content": message.content,
      "timestamp": message.timestamp.isoformat(),
      "sender": message.sender.username
    }
    for message in messages
  ]
  print('messages_data:', room.messages)
  return templates.TemplateResponse(
    "send_message.html",
    {
      "request": request,
      "room": room,
      "messages": messages_data
    }
  )

@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
  return templates.TemplateResponse(
      request=request, name="index.html"
  )

@router.get('/messages', response_model=List[MessageResponse])
async def get_all_messages(db: Session = Depends(get_session_db), token: str = Depends(get_current_user)):
  messages = get_messages(db)
  if not messages:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Сообщений не найдено')
  raise messages

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

@router.get('/rooms/{room_id}', response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_session_db)):
    room = get_room_by_id(db, id=room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Комната не найдена')
    return room

@router.delete('/rooms/{room_id}/users/{user_id}')
def remove_user_from_room(room_id: int, user_id: int, db: Session = Depends(get_session_db)):
  room = get_room_by_id(db, id=room_id)
  if not room:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Комната не найдена')

  user = get_user(db, user_id=user_id)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

  remove_user_from_room(db, room_id=room_id, user_id=user_id)
  return {'detail': 'User removed from room'}