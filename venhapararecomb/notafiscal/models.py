from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    identificador = models.CharField(max_length=14) # cpf ou cnpj
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

class Boleto(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

class NotaFiscal(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    clientes = models.ManyToManyField(Cliente)
    boletos = models.ManyToManyField(Boleto)
