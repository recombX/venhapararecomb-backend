from django.test import TestCase
from django.urls import reverse
from .models import Fornecedor, NotaFiscal, Cliente, Boleto, Endereco

FORNECEDOR_NOME = 'Fornecedor Test'
FORNECEDOR_CNPJ = '12345678901234'
NF_IDENTIFICADOR = 'NF001'
CLIENTE_NOME = 'Cliente Test'
CLIENTE_TIPO_DOCUMENTO = 'CPF'
CLIENTE_DOCUMENTO = '12345678901'
BOLETO_VALOR = 100.00
BOLETO_DATA_VENCIMENTO = '2024-01-01'

class ModelTestCase(TestCase):
    def setUp(self):
        self.fornecedor = Fornecedor.objects.create(nome=FORNECEDOR_NOME, cnpj=FORNECEDOR_CNPJ)
        self.endereco = Endereco.objects.create(logradouro='Rua Test', numero='123', bairro='Bairro Test',
                                                 cidade='Cidade Test', estado='TS', cep='12345678',
                                                 pais='País Test', telefone='123456789')
        self.cliente = Cliente.objects.create(nome=CLIENTE_NOME, tipo_documento=CLIENTE_TIPO_DOCUMENTO, documento=CLIENTE_DOCUMENTO,
                                               endereco=self.endereco)
        self.nf = NotaFiscal.objects.create(identificador=NF_IDENTIFICADOR, fornecedor=self.fornecedor)
        self.boleto = Boleto.objects.create(valor=BOLETO_VALOR, data_vencimento=BOLETO_DATA_VENCIMENTO, nota_fiscal=self.nf)

    def test_fornecedor_creation(self):
        self.assertEqual(self.fornecedor.nome, FORNECEDOR_NOME)
        self.assertEqual(self.fornecedor.cnpj, FORNECEDOR_CNPJ)

    def test_nota_fiscal_creation(self):
        self.assertEqual(self.nf.identificador, NF_IDENTIFICADOR)
        self.assertEqual(self.nf.fornecedor, self.fornecedor)

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nome, CLIENTE_NOME)
        self.assertEqual(self.cliente.tipo_documento, CLIENTE_TIPO_DOCUMENTO)
        self.assertEqual(self.cliente.documento, CLIENTE_DOCUMENTO)
        self.assertEqual(self.cliente.endereco, self.endereco)

    def test_boleto_creation(self):
        self.assertEqual(self.boleto.valor, BOLETO_VALOR)
        self.assertEqual(str(self.boleto.data_vencimento), BOLETO_DATA_VENCIMENTO)
        self.assertEqual(self.boleto.nota_fiscal, self.nf)


class ViewTestCase(TestCase):
    def setUp(self) :
        self.fornecedor = Fornecedor.objects.create(nome=FORNECEDOR_NOME, cnpj=FORNECEDOR_CNPJ)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_list_nfs_view(self):
        response = self.client.get(reverse('list_nfs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_nfs.html')

    def test_detail_nf_view(self):
        nf = NotaFiscal.objects.create(identificador=NF_IDENTIFICADOR, fornecedor=self.fornecedor)
        response = self.client.get(reverse('detail_nf', args=(nf.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_nf.html')

    def test_delete_nf_view(self):
        nf = NotaFiscal.objects.create(identificador=NF_IDENTIFICADOR, fornecedor=self.fornecedor)
        response = self.client.post(reverse('delete_nf', args=(nf.id,)))
        self.assertEqual(response.status_code, 302)

    def test_list_clientes_view(self):
        response = self.client.get(reverse('list_clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_clientes.html')

    def test_list_forncedores_view(self):
        response = self.client.get(reverse('list_fornecedores'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_fornecedores.html')

    def test_delete_fornecedor_view(self):
        response = self.client.post(reverse('delete_fornecedor', args=(self.fornecedor.id,)))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_cliente_view(self):
        cliente = Cliente.objects.create(nome=CLIENTE_NOME, tipo_documento=CLIENTE_TIPO_DOCUMENTO, documento=CLIENTE_DOCUMENTO,
                                               endereco=Endereco.objects.create(logradouro='Rua Test', numero='123', bairro='Bairro Test',
                                                 cidade='Cidade Test', estado='TS', cep='12345678',
                                                 pais='País Test', telefone='123456789'))
        response = self.client.post(reverse('delete_cliente', args=(cliente.id,)))
        self.assertEqual(response.status_code, 302)
    


