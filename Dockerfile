From python:latest

copy ./requirements.txt .

run pip install -r requirements.txt

copy ./testes /testes

copy service.py .

copy database.py .

copy parsing.py .

copy home.html .

expose 5000

cmd python service.py testes/teste.xml