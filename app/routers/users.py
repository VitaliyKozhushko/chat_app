from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.crud import get_user_by_username, create_user, get_user, get_all_users
from app.schemas import UserResponse, UserCreate, UserBase
from app.database import get_session_db
from app.auth import get_current_user
from app.sockets import users
from typing import List

router = APIRouter()

@router.get('/users', response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_session_db)):
  rooms = get_all_users(db, skip=skip, limit=limit)
  if not rooms:
    return JSONResponse(content={
      'message': 'Созданных комнат нет'
    })
  return rooms

@router.get("/online-users", response_model=List[str])
async def get_online_users():
  print(users)
  return [user_id for user_id, info in users.items() if info['online']]
