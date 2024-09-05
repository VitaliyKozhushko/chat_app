from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=True)
  hashed_password = Column(String, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  messages = relationship('Message', back_populates='sender')

class Message(Base):
  __tablename__ = 'messages'

  id = Column(Integer, primary_key=True, index=True)
  content = Column(Text, nullable=False)
  timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  sender_id = Column(Integer, ForeignKey('users.id'))

  sender = relationship('User', back_populates='messages')