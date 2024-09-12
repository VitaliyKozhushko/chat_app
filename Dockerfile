FROM python:3.10-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:socketio_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
