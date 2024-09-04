from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, crud, database
from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUT = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_passwd(plain_passwd, hashed_passwd):
  return passwd_context.verify(plain_passwd, hashed_passwd)

def create_passwd_hash(passwd):
  return passwd_context.hash(passwd)

def auth_user(db: Session, username: str, passwd: str):
  user = crud.get_user_by_username(db, username)
  if not user or not verify_passwd(passwd, user.hashed_password):
    return False
  return user

def verify_token(db: Session, token: str):
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username = payload.get("sub")
      if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
      user = crud.get_user_by_username(db, username)
      return user
    except jwt.PyJWTError:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUT)
  to_encode.update({'exp': expire})
  encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encode_jwt

def create_refresh_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(db: Session = Depends(database.get_session_db), token: str = Depends(oauth2_scheme)):
  credintial_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Не удалось проверить учетные данные',
    headers={'WWW-Authenticate': 'Bearer'}
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: str = payload.get('sub')
    if username is None:
      raise credintial_exception
  except jwt.ExpiredSignatureError:
    raise credintial_exception
  except jwt.InvalidTokenError:
    raise credintial_exception
  user = crud.get_user_by_username(db, username=username)
  if user is None:
    raise credintial_exception
  return user

def get_current_active_user(current_user: schemas.UserResponse = Depends(get_current_user)):
  return current_user