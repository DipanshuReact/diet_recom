# backend/Dockerfile

FROM python:3.10.8

RUN mkdir -p app/backend

WORKDIR /app/backend

COPY FastAPI_Backend/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY Data ../Data

COPY FastAPI_Backend .

EXPOSE 8080

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080","--reload"]