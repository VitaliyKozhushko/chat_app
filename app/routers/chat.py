from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_session_db
from app.schemas import MessageResponse, MessageCreate
from app.auth import get_current_user
from app.crud import get_user, create_message, get_messages

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