from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

room_users = Table(
  'room_users',
  Base.metadata,
  Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
  Column('room_id', Integer, ForeignKey('rooms.id'), primary_key=True),
  extend_existing=True
)


class Room(Base):
  __tablename__ = 'rooms'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, index=True)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  # Определяем отношение многие-ко-многим через таблицу room_users
  users = relationship('User', secondary=room_users, back_populates='rooms')
  messages = relationship('Message', back_populates='room')


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=True)
  hashed_password = Column(String, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  rooms = relationship('Room', secondary=room_users, back_populates='users')

  messages = relationship('Message', back_populates='sender')

class Message(Base):
  __tablename__ = 'messages'
  id = Column(Integer, primary_key=True, index=True)
  content = Column(Text, nullable=False)
  timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  sender_id = Column(Integer, ForeignKey('users.id'))
  room_id = Column(Integer, ForeignKey('rooms.id'))

  sender = relationship('User', back_populates='messages')

  room = relationship('Room', back_populates='messages')
