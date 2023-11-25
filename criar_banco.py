'''Creates the database with tables referring to the defined classes''' 
from recomb import database, app
from recomb.models import Fornecedor, Cliente, Endereco, Nota

with app.app_context():
    database.create_all()
    