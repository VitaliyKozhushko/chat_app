from sqlalchemy.orm import Session, joinedload
from . import models, schemas
from passlib.context import CryptContext

passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
  hashed_passwd = passwd_context.hash(user.password)
  db_user = models.User(username=user.username, hashed_password=hashed_passwd)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def create_message(db:Session, message: schemas.MessageCreate, user_id: int, room_id: int):
  db_message = models.Message(
    content=message.content,
    sender_id=user_id,
    room_id=room_id
  )
  db.add(db_message)
  db.commit()
  db.refresh(db_message)
  return db_message

def get_messages(db: Session, skip: int = 0, limit: int = 10):
  return db.query(models.Message).offset(skip).limit(limit).all()

def create_new_room(db: Session, name: str):
  db_room = models.Room(name=name)
  db.add(db_room)
  db.commit()
  db.refresh(db_room)
  return db_room

def get_room_by_id(db: Session, id: int):
  return db.query(models.Room).filter_by(id=id).first()

def get_room_by_name(db: Session, name: str):
  return db.query(models.Room).filter(models.Room.name == name).first()

def get_all_rooms(db: Session, skip: int = 0, limit: int = 10):
  return (
    db.query(models.Room)
    .options(joinedload(models.Room.users))
    .offset(skip)
    .limit(limit)
    .all()
  )

def remove_user_from_room(db: Session, room_id: int, user_id: int):
  db_room_user = db.query(models.RoomUser).filter(models.RoomUser.user_id == user_id, models.RoomUser.room_id == room_id).first()
  if db_room_user:
    db.delete(db_room_user)
    db.commit()
  return db_room_user

def get_room_messages(db: Session, id: int):
  return db.query(models.Room).filter(models.Room.id == id).options(
    joinedload(models.Room.messages).joinedload(models.Message.sender)
  ).first()