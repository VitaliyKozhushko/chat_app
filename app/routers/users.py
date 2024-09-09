from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import get_user_by_username, create_user, get_user
from app.schemas import UserResponse, UserCreate, UserBase
from app.database import get_session_db
from app.auth import get_current_user
from app.sockets import users
from typing import List

router = APIRouter()

@router.get('/users/me', response_model=UserResponse)
async def get_current_user(current_user: UserResponse = Depends(get_current_user)):
  return current_user

@router.put('/users/me', response_model=UserResponse)
async def update_current_user(update_user: UserBase, db: Session = Depends(get_session_db), current_user: UserResponse = Depends(get_current_user)):
  user = get_user(db, user_id=current_user.id)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
  user.username = update_user.username or user.username
  db.commit()
  db.refresh()

  return user

@router.get("/online-users", response_model=List[str])
async def get_online_users():
  print(users)
  return [user_id for user_id, info in users.items() if info['online']]
