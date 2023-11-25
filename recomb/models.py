'''Creates the database structure'''
from recomb import database

class Fornecedor(database.Model):
    '''Class representing a supplier'''

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    documento = database.Column(database.String, nullable=False, unique=True)
    nota = database.relationship("Nota", backref="fornecedor", lazy=True)

class Cliente(database.Model):
    '''Class representing a client'''

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    documento = database.Column(database.String, nullable=False, unique=True)
    endereco = database.relationship("Endereco", backref="cliente", lazy=True)
    nota = database.relationship("Nota", backref="cliente", lazy=True)

class Endereco(database.Model):
    '''Class representing a address'''

    id = database.Column(database.Integer, primary_key=True)
    rua = database.Column(database.String, nullable=False)
    num = database.Column(database.Integer, nullable=False)
    bairro = database.Column(database.String, nullable=False)
    municipio = database.Column(database.String, nullable=False)
    uf = database.Column(database.String, nullable=False)
    cep = database.Column(database.String, nullable=False)
    pais = database.Column(database.String, nullable=False)
    telefone = database.Column(database.Integer, nullable=False)
    id_cliente = database.Column(database.Integer, database.ForeignKey('cliente.id'),
                                 nullable=False)

class Nota(database.Model):
    '''Class representing a invoice'''

    id = database.Column(database.Integer, primary_key=True)
    valor = database.Column(database.Integer, nullable=False)
    vencimento = database.Column(database.String, nullable=False)
    num_nota = database.Column(database.Integer, nullable=False)
    id_cliente = database.Column(database.Integer,
                                 database.ForeignKey('cliente.id'), nullable=False)
    id_fornecedor = database.Column(database.Integer,
                                    database.ForeignKey('fornecedor.id'), nullable=False)
