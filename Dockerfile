FROM python:3.9
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload 