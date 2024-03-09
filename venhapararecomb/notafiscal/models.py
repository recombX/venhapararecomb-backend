from typing import Any
from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)

    def __str__(self) -> str:
        return self.nome

class NotaFiscal(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Nota Fiscal {self.fornecedor.nome}'

class Boleto(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Boleto {self.valor} - {self.data_vencimento}'

class Cliente(models.Model):
    TIPO_DOCUMENTO = (
        ('CPF', 'CPF'),
        ('CNPJ', 'CNPJ'),
    )

    nome = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO)
    documento = models.CharField(max_length=14) # cpf ou cnpj
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

    


   
