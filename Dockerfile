# Use a imagem oficial do Python como base
FROM python:3.8

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de requisitos e o código da aplicação para o diretório de trabalho
COPY requirements.txt .
COPY . .

# Instale as dependências
RUN pip install -r requirements.txt

# Exponha a porta na qual o servidor Flask estará rodando
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["python", "run.py"]
