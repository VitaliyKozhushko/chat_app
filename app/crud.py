from sqlalchemy import Session
from . import models, schemas
from fastapi import HTTPException, status
from passlib.context import CryptContext

passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
  hashed_passwd = passwd_context.hash(user.password)
  db_user = models.User(username=user.username, hashed_password=hashed_passwd)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def create_message(db:Session, message: schemas.MessageCreate, user_id: int):
  db_message = models.Message(content=message.content, sender_id=user_id)
  db.add(db_message)
  db.commit()
  db.refresh(db_message)
  return db_message

def get_messages(db: Session, skip: int = 0, limit: int = 10):
  return db.query(models.Message).offset(skip).limit(limit).all()