from django.contrib import admin
from .models import Fornecedor, Cliente, Boleto, NotaFiscal

admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Boleto)
admin.site.register(NotaFiscal)
