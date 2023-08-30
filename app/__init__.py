from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Importar rotas e modelos após criar a instância do Flask
from app.routes import MainRoute, NotaFiscalRoute, ClienteRoute, DuplicataRoute, FornecedorRoute
from app.models import Cliente, Duplicata, Fornecedor, NotaFiscal

# Crie as tabelas no banco de dados
with app.app_context():
    db.create_all()