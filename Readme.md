# Тестовое задание

Создать api приложение на FastAPI с использованием SocketIO для чата в реальном времени
<hr>

## Содержание

1. [Требования](#main_requirements)
2. [Стек технологий](#technology_stack)
3. [Документация по API](#doc_api)
4. [Требования к проекту со стороны фронтенда](#front_requirements)
4. [Инструкция по запуску проекта](#instruction_startup)
5. [Особенности](#features)

## Требования <a name="main_requirements"></a>

- Основная функциональность:
  - Пользователи могут подключаться к чату и отправлять сообщения. 
  - Все подключенные пользователи видят все отправленные сообщения в
  реальном времени. 
  - Реализовать простую аутентификацию пользователей (например, с
  помощью токенов). 
  - Использовать базу данных для хранения истории сообщений (например,
  PostgreSQL или SQLite).

- Дополнительные требования:
  - Добавить комнаты чата, где пользователи могут выбирать, в какой
  комнате общаться. 
  - Реализовать приватные сообщения между пользователями. 
  - Добавить уведомления о новых сообщениях.

## Стэк технологий <a name="technology_stack"></a>

- Backend: [FastAPI](https://fastapi.tiangolo.com/)
- Authentication: [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- Database: [SQLite](https://www.sqlite.org/)
- Real-time communication: [SocketIO](https://python-socketio.readthedocs.io/en/stable/)
- Frontend: [VueJS](https://vuejs.org/)
- UI Library: [Element+](https://element-plus.org/en-US/)
- State management: [Vuex](https://v3.vuex.vuejs.org/ru/)
- Logo: YandexGPT + [Шедеврум](https://shedevrum.ai/)

## Документация по API <a name="doc_api"></a>

- Swagger: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

## Требования к проекту со стороны фронтенда <a name="front_requirements"></a>

- NodeJS v.20.17.0
- NPM v.10.8.2

## Инструкция по запуску проекта <a name="instruction_startup"></a>

1. Клонируйте репозиторий
```
git clone https://github.com/VitaliyKozhushko/chat_app
```
2. Настройте .env файл
3. Запустите проект:
   - либо с помощью команд FastAPI:
   ```
    uvicorn app.main:socketio_app --reload
    ```
   - в другом терминале, находясь в папке проекта перейти в папку frontend
   ```
   npm run dev
   ```
   - перейти по ссылке localhost фронтенда<br>
   ====
   - либо с помощью Docker
    ```
    docker compose up --build -d
    ```

## Особенности <a name="features"></a>

- перед первым входом необходимо зарегистрироваться
- адаптивность не добавлена
- создавать комнаты может любой пользователь
- для вступления в комнату надо нажать "Присоединиться"
- для выхода из комнаты (удаление из списка, в которых состоит пользователь) - "Покинуть"
- в БД сохраняется история как сообщений внутри комнат, так и приватных сообщений
- уведомления отображаются только для пользователей, которые онлайн