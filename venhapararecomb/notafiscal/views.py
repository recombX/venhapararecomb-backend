from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .models import Fornecedor, Cliente, Boleto, NotaFiscal


def parse_xml(xml_file):
    xml = ET.parse(xml_file)
    root = xml.getroot()
    nsNFe = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    xNome = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe).text
    cnpj = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe).text
    fornecedor = {'nome': xNome, 'cnpj': cnpj}

    clientes = []
    for dest in root.findall('ns:NFe/ns:infNFe/ns:dest', nsNFe):
        xNome = dest.find('ns:xNome', nsNFe).text
        cpf = dest.find('ns:CPF', nsNFe)
        cnpj = dest.find('ns:CNPJ', nsNFe)

        documento = cpf.text if cpf is not None else cnpj.text
        tipo_documento = 'CPF' if cpf is not None else 'CNPJ'

        clientes.append({'nome': xNome, 'documento': documento, 'tipo_documento': tipo_documento})

    boletos = []
    for det in root.findall('ns:NFe/ns:infNFe/ns:cobr/ns:dup', nsNFe):
        valor = det.find('ns:vDup', nsNFe).text
        data_vencimento = det.find('ns:dVenc', nsNFe).text
        boletos.append({'valor': valor, 'data_vencimento': data_vencimento})

    return {'fornecedor': fornecedor, 'clientes': clientes, 'boletos': boletos}


def index(request):
    context = {}

    if request.method == 'POST':
        if 'read_xml' in request.POST:
            xml_data = parse_xml(request.FILES['xml_file'])
            request.session['xml_data'] = xml_data
            context['xml_data'] = xml_data

        elif 'save_nf' in request.POST:
            xml_data = request.session.pop('xml_data', {})

            fornecedor, _ = Fornecedor.objects.get_or_create(nome=xml_data['fornecedor']['nome'], cnpj=xml_data['fornecedor']['cnpj'])
            nf = NotaFiscal.objects.create(fornecedor=fornecedor)

            for cliente in xml_data['clientes']:
                Cliente.objects.create(nome=cliente['nome'], documento=cliente['documento'], tipo_documento=cliente['tipo_documento'], nota_fiscal=nf)

            for boleto in xml_data['boletos']:
                Boleto.objects.create(valor=boleto['valor'], data_vencimento=boleto['data_vencimento'], nota_fiscal=nf)
          
            return redirect('index')

    return render(request, 'index.html', context)
