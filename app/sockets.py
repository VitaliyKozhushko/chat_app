import socketio
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .database import get_session_db
from .crud import get_user_by_username, create_message
from .schemas import MessageCreate, MessageResponse

sio = socketio.AsyncServer(async_mode='asgi')

socket_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ, auth):
  db: Session = next(get_session_db())

  token = auth.get('token')
  if not token:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

  user = get_user_by_username(db, token)  # Предполагается, что token это username (для простоты тестового задания)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

  print(f"User {user.username} connected with session id {sid}")
  await sio.save_session(sid, {'user_id': user.id, 'username': user.username})

@sio.event
async def disconnect(sid):
  session = await sio.get_session(sid)
  username = session.get('username')
  print(f"User {username} disconnected")


@sio.event
async def send_message(sid, data):
  session = await sio.get_session(sid)
  user_id = session.get('user_id')
  username = session.get('username')

  db: Session = next(get_session_db())

  try:
    message_data = MessageCreate(**data)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message data")

  message = create_message(db, message_data, user_id)

  room = data.get('room_id')
  response = MessageResponse(
    id=message.id,
    content=message.content,
    timestamp=message.timestamp,
    sender_id=message.sender_id
  )

  await sio.emit('new_message', response.dict(), room=room)
  print(f"User {username} sent message to room {room}")


@sio.event
async def join_room(sid, data):
  room = data['room']
  await sio.enter_room(sid, room)
  print(f"Session {sid} joined room {room}")


@sio.event
async def leave_room(sid, data):
  room = data['room']
  await sio.leave_room(sid, room)
  print(f"Session {sid} left room {room}")
