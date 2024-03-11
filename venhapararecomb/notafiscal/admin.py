from django.contrib import admin
from .models import Fornecedor, Cliente, Boleto, NotaFiscal, Endereco

admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Boleto)
admin.site.register(NotaFiscal)
admin.site.register(Endereco)
