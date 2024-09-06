import socketio
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .database import get_session_db
from .crud import create_message
from .auth import verify_token
from .schemas import MessageCreate, MessageResponse
from .models import Room, User

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ):
    query_string = environ.get('QUERY_STRING', '')
    query_params = dict(x.split('=') for x in query_string.split('&'))
    token = query_params.get('auth_token')

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

    db: Session = next(get_session_db())

    user = verify_token(db, token)
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
    sender_id=message.sender_id,
    username=username
  )
  await sio.emit('new_message', response.model_dump_json(), room=room)
  print(f"User {username} sent message to room {room}")

@sio.event
async def leave_room(sid, data):
  room = data['room']
  await sio.leave_room(sid, room)
  print(f"Session {sid} left room {room}")

@sio.event
async def connect_room(sid, data):
  user_id = data.get('user_id')
  room_id = data.get('room_id')

  db: Session = next(get_session_db())

  room = db.query(Room).filter(Room.id == room_id).first()
  if not room:
    return {"error": "Room not found"}

  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    return {"error": "User not found"}

  if user not in room.users:
      room.users.append(user)
      db.commit()

  await sio.enter_room(sid, room_id)
  print(f"User {user_id} joined room {room_id}")

  await sio.emit('user_joined', {'user_id': user_id, 'room_id': room_id}, room=room_id)

@sio.event
async def leave_room(sid, room_id):
    await sio.leave_room(sid, room_id)
    print(f"User {sid} left room {room_id}")

@sio.event
async def join_room(sid, room):
    await sio.enter_room(sid, room)
    print(f"Client {sid} joined room {room}")