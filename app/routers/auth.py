from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import auth, schemas, crud, database

router = APIRouter()

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_session_db)):
  user = auth.auth_user(db, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Неверный логин или пароль',
      headers={'WWW_Authenticate': "Bearer"}
    )
  access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUT)
  access_token = auth.create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
  refresh_token = auth.create_refresh_token(data={'sub': user.username})
  return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

@router.post('/registration', response_model=schemas.UserResponse)
def registration(user: schemas.UserCreate, db: Session = Depends(database.get_session_db)):
  existing_user = crud.get_user_by_username(db, username=user.username)
  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='Пользователь с таким логином уже зарегистрирован'
    )
  user = crud.create_user(db, user)
  return user
