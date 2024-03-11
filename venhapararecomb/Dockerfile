# Imagem base do Python
FROM python:3.10

# Configuração do diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Copia o restante do código-fonte para o contêiner
COPY . .

# Expõe a porta 8000 do contêiner
EXPOSE 8000

# Comando para executar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
