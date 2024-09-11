import socketio
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .database import get_session_db
from .crud import create_message
from .auth import verify_token
from .schemas import MessageCreate, MessageResponse
from .models import Room, User
from datetime import datetime

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

users = {}

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
  for user_id, info in users.items():
    if info['sid'] == sid:
      users[user_id]['online'] = False
      print(f"Пользователь {user_id} отключен")
      break

# отправка сообщения в комнате
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

  room_id = data.get('room_id')
  message = create_message(db, message_data, user_id, room_id)

  response = MessageResponse(
    id=message.id,
    content=message.content,
    timestamp=message.timestamp,
    sender_id=message.sender_id,
    sender=username
  )
  await sio.emit('send_message', response.model_dump_json(), room=room_id)
  print(f"User {username} sent message to room {room_id}")

# удаление пользователя из комнаты
@sio.event
async def disconnect_room(sid, data):
  user_id = data.get('user_id')
  room_id = data.get('room_id')

  db: Session = next(get_session_db())

  room = db.query(Room).filter(Room.id == room_id).first()
  if not room:
    await sio.emit('disconnect_room', {'error': 'Комната не найдена'}, to=sid)
    return

  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    await sio.emit('disconnect_room', {'error': 'Пользователь не найден'}, to=sid)
    return

  if user in room.users:
    room.users.remove(user)
    db.commit()

  print(sid)
  print(f"User {user_id} left room {room_id}")
  await sio.emit('disconnect_room', {
    'message': f'Пользователь {user_id} удален из комнаты {room_id}',
    'room_id': room_id,
    'user_id': user_id
  }, to=sid)
  # await sio.emit('user_left', {'user_id': user_id, 'username': user.username}, room=room_id)

# добавление пользователя в комнату
@sio.event
async def connect_room(sid, data):
  user_id = data.get('user_id')
  room_id = data.get('room_id')

  db: Session = next(get_session_db())

  room = db.query(Room).filter(Room.id == room_id).first()
  if not room:
    await sio.emit('connect_room', {'error': 'Комната не найдена'}, to=sid)
    return

  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    await sio.emit('connect_room', {'error': 'Пользователь не найден'}, to=sid)
    return

  if user not in room.users:
    room.users.append(user)
    db.commit()

  await sio.emit('connect_room', {
    'message': f'Пользователь {user_id} добавлен в комнату {room_id}',
    'room_id': room_id,
    'user_id': user_id
  }, to=sid)

# вход пользователя в комнату
@sio.event
async def join_room(sid, room, user_id):
    db: Session = next(get_session_db())
    user = db.query(User).filter(User.id == user_id).first()
    await sio.enter_room(sid, room)
    await sio.emit(
      'user_joined',
      {'user_id': user_id, 'username': user.username},
      room=room,
    )
    print(f"Client {sid} joined room {room}")

# выход пользователя из комнаты
@sio.event
async def leave_room(sid, room, user_id):
  db: Session = next(get_session_db())
  user = db.query(User).filter(User.id == user_id).first()
  await sio.leave_room(sid, room)
  await sio.emit('user_left', {'user_id': user_id, 'username': user.username}, room=room)

@sio.event
async def register(sid, user_id):
    db: Session = next(get_session_db())
    user = db.query(User).filter(User.id == user_id).first()
    users[user_id] = {'sid': sid, 'online': True, 'sender': user.username}
    print(f"Пользователь {user_id} зарегистрирован с sid {sid}")
    await sio.emit('register', {'user_id': user_id}, to=sid)

@sio.event
async def private_message(sid, data):
    to_user_id = str(data['to'])
    from_user_id = str(data['from'])
    message = data['message']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if to_user_id in users and users[to_user_id]['online']:
        to_sid = users[to_user_id]['sid']
        from_sid = users[from_user_id]['sid']
        await sio.emit('private_message', {
          'id': now,
          'sender': users[from_user_id]['sender'],
          'sender_id': from_user_id,
          'content': message}, room=to_sid)
        await sio.emit('private_message', {
          'id': now,
          'sender': users[from_user_id]['sender'],
          'sender_id': from_user_id,
          'content': message}, room=from_sid)