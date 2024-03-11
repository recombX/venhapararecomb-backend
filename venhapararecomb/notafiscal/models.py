from typing import Any
from django.db import models

class Fornecedor(models.Model):
    """
    Modelo que representa um fornecedor de produtos. Cada fornecedor possui um nome e um CNPJ.
    """
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)

    def __str__(self) -> str:
        return self.nome

class NotaFiscal(models.Model):
    """
    Modelo que representa uma nota fiscal. Cada nota fiscal possui um identificador único, um fornecedor e uma lista de clientes.
    """
    identificador = models.CharField(max_length=50, unique=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    clientes = models.ManyToManyField('Cliente', related_name='notas_fiscais')

    def __str__(self) -> str:
        return f'Nota Fiscal {self.id} - {self.fornecedor}'

class Boleto(models.Model):
    """
    Modelo que representa um boleto. Cada boleto possui um valor, uma data de vencimento e uma nota fiscal.
    """
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Boleto {self.valor} - {self.data_vencimento}'

class Endereco(models.Model):
    """
    Modelo que representa um endereço. Cada endereço possui um logradouro, um número, um bairro, uma cidade, um estado, um CEP, um país e um telefone.
    """
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    pais = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.logradouro

class Cliente(models.Model):
    """
    Modelo que representa um cliente. Cada cliente possui um nome, um tipo de documento (CPF ou CNPJ), um documento (CPF ou CNPJ) e um endereço.
    """
    TIPO_DOCUMENTO = (
        ('CPF', 'CPF'),
        ('CNPJ', 'CNPJ'),
    )

    nome = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO)
    documento = models.CharField(max_length=14, unique=True) # cpf ou cnpj
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome 
