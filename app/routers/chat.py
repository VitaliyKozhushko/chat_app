from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_session_db
from app.schemas import MessageResponse, MessageCreate, RoomResponse, RoomCreate
from app.auth import get_current_user
from app.crud import get_user, create_message, get_messages, get_room_by_name, create_room, get_room_by_id

router = APIRouter()

@router.post('/messages', response_model=MessageResponse)
async def send_message(message: MessageCreate, db: Session = Depends(get_session_db), token: str = Depends(get_current_user)):
  user = get_user(db, user_id=token.id)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
  new_message = create_message(db=db, message=message,user_id=user.id)
  return new_message

@router.get('/messages', response_model=List[MessageResponse])
async def get_all_messages(db: Session = Depends(get_session_db), token: str = Depends(get_current_user)):
  messages = get_messages(db)
  if not messages:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Сообщений не найдено')
  raise messages

@router.post('/rooms', response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_session_db)):
    existing_room = get_room_by_name(db, name=room.name)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Комната с таким названием уже существует'
        )
    new_room = create_room(db, name=room.name)
    return new_room

@router.get('/rooms/{room_id}', response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_session_db)):
    room = get_room_by_id(db, id=room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Комната не найдена')
    return room


@router.post('/rooms/{room_id}/users/{user_id}')
def add_user_to_room(room_id: int, user_id: int, db: Session = Depends(get_session_db)):
  room = get_room_by_id(db, id=room_id)
  if not room:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Комната не найдена')

  user = get_user(db, user_id=user_id)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

  add_user_to_room(db, room_id=room_id, user_id=user_id)
  return {'detail': 'User added to room'}


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