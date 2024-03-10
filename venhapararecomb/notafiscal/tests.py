from django.test import TestCase
from django.urls import reverse
from .models import Fornecedor, NotaFiscal, Cliente, Boleto, Endereco

class ModelTestCase(TestCase):
    def setUp(self):
        self.fornecedor = Fornecedor.objects.create(nome='Fornecedor Test', cnpj='12345678901234')
        self.endereco = Endereco.objects.create(logradouro='Rua Test', numero='123', bairro='Bairro Test',
                                                 cidade='Cidade Test', estado='TS', cep='12345678',
                                                 pais='País Test', telefone='123456789')
        self.cliente = Cliente.objects.create(nome='Cliente Test', tipo_documento='CPF', documento='12345678901',
                                               endereco=self.endereco)
        self.nf = NotaFiscal.objects.create(identificador='NF001', fornecedor=self.fornecedor)
        self.boleto = Boleto.objects.create(valor=100.00, data_vencimento='2024-12-31', nota_fiscal=self.nf)

    def test_fornecedor_creation(self):
        self.assertEqual(self.fornecedor.nome, 'Fornecedor Test')
        self.assertEqual(self.fornecedor.cnpj, '12345678901234')

    def test_nota_fiscal_creation(self):
        self.assertEqual(self.nf.identificador, 'NF001')
        self.assertEqual(self.nf.fornecedor, self.fornecedor)

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nome, 'Cliente Test')
        self.assertEqual(self.cliente.tipo_documento, 'CPF')
        self.assertEqual(self.cliente.documento, '12345678901')
        self.assertEqual(self.cliente.endereco, self.endereco)

    def test_boleto_creation(self):
        self.assertEqual(self.boleto.valor, 100.00)
        self.assertEqual(str(self.boleto.data_vencimento), '2024-12-31')
        self.assertEqual(self.boleto.nota_fiscal, self.nf)


class ViewTestCase(TestCase):
    def setUp(self) :
        self.fornecedor = Fornecedor.objects.create(nome='Fornecedor Test', cnpj='12345678901234')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_list_nfs_view(self):
        response = self.client.get(reverse('list_nfs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_nfs.html')

    def test_detail_nf_view(self):
        nf = NotaFiscal.objects.create(identificador='NF002', fornecedor=self.fornecedor)
        response = self.client.get(reverse('detail_nf', args=(nf.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_nf.html')

    def test_delete_nf_view(self):
        nf = NotaFiscal.objects.create(identificador='NF003', fornecedor=self.fornecedor)
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
        cliente = Cliente.objects.create(nome='Cliente Test', tipo_documento='CPF', documento='12345678901',
                                               endereco=Endereco.objects.create(logradouro='Rua Test', numero='123', bairro='Bairro Test',
                                                 cidade='Cidade Test', estado='TS', cep='12345678',
                                                 pais='País Test', telefone='123456789'))
        response = self.client.post(reverse('delete_cliente', args=(cliente.id,)))
        self.assertEqual(response.status_code, 302)
    


