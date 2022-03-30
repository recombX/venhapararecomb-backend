from datetime import datetime

class Fornecedor():
    """
    Class that represents a fornecedor.

    Attributes:
        identificador (str): The fornecedor's identifier.
    """
    def __init__(self, identificador):
        self.identificador = identificador

class Cliente():
    """
    Class that represents a cliente.

    Attributes:
        identificador (str): The cliente's identifier.
        nome (str): The cliente's name.
        endereco (str): The cliente's address.
    """
    def __init__(self, identificador, nome, endereco):
        self.identificador = identificador
        self.nome = nome
        self.endereco = endereco

class NotaFiscal():
    """
    Class that represents a nota fiscal.

    Attributes:
        fornecedor (Fornecedor): The fornecedor of the nota fiscal.
        cliente (Cliente): The cliente of the nota fiscal.
        boletos (list): The list of boletos of the nota fiscal.
    """
    def __init__(self, fornecedor, cliente, boletos):
        self.fornecedor = fornecedor
        self.cliente = cliente
        self.boletos = boletos
