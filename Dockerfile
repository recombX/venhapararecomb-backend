# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app
ENV FLASK_APP main.py

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python criar_banco.py

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

