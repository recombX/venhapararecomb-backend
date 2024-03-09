from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.shortcuts import redirect
from .models import Fornecedor, Cliente, Boleto, NotaFiscal
import json


def index(request):
    xml_data = {}
    
    if request.method == 'POST':
        if 'read_xml' in request.POST:
            xml = ET.parse(request.FILES['xml_file'])
            root = xml.getroot()
            nsNFe = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
            # recuperando o nome e o cnpj do fornecedor
            xNome = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe).text
            cnpj = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe).text
            #fornecedor, created = Fornecedor.objects.get_or_create(nome=xNome, cnpj=cnpj)
            fornecedor = {'nome': xNome, 'cnpj': cnpj}
            
            # recuperando o nome e o cpf ou cnpj dos clientes
            clientes = []
            for dest in root.findall('ns:NFe/ns:infNFe/ns:dest', nsNFe):
                xNome = dest.find('ns:xNome', nsNFe).text
                cpf = dest.find('ns:CPF', nsNFe)
                cnpj = dest.find('ns:CNPJ', nsNFe)
                if cpf is not None:
                    ident = cpf.text
                else:
                    ident = cnpj.text
                clientes.append({'nome': xNome, 'identificador': ident})
            
                #cliente, created = Cliente.objects.get_or_create(nome=xNome, identificador=ident, fornecedor=fornecedor)
            boletos = []
            for det in root.findall('ns:NFe/ns:infNFe/ns:cobr/ns:dup', nsNFe):
                valor = det.find('ns:vDup', nsNFe).text
                data_vencimento = det.find('ns:dVenc', nsNFe).text
                boletos.append({'valor': valor, 'data_vencimento': data_vencimento})
                #boleto = Boleto.objects.create(valor=valor, data_vencimento=data_vencimento, fornecedor=fornecedor)
                xml_data = {'fornecedor': fornecedor, 'clientes': clientes, 'boletos': boletos}
                request.session['xml_data'] = xml_data

        elif 'save_nf' in request.POST:
            xml_data = request.session.get('xml_data', {})
           
            fornecedor, created = Fornecedor.objects.get_or_create(nome=xml_data['fornecedor']['nome'], cnpj=xml_data['fornecedor']['cnpj'])
            
            for cliente in xml_data['clientes']:
                Cliente.objects.create(nome=cliente['nome'], identificador=cliente['identificador'], fornecedor=fornecedor)
            for boleto in xml_data['boletos']:
                Boleto.objects.create(valor=boleto['valor'], data_vencimento=boleto['data_vencimento'], fornecedor=fornecedor)
            
            nf=NotaFiscal.objects.create(fornecedor=fornecedor)
            nf.clientes.set(Cliente.objects.filter(fornecedor=fornecedor))
            nf.boletos.set(Boleto.objects.filter(fornecedor=fornecedor))

            return redirect('index')
            
    return render(request, 'index.html', {'xml_data': xml_data})





