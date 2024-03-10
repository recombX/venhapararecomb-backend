from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .models import Fornecedor, Cliente, Boleto, NotaFiscal, Endereco


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

        endereco = dest.find('ns:enderDest', nsNFe)
        logradouro = endereco.find('ns:xLgr', nsNFe).text
        numero = endereco.find('ns:nro', nsNFe).text
        bairro = endereco.find('ns:xBairro', nsNFe).text
        cidade = endereco.find('ns:xMun', nsNFe).text
        estado = endereco.find('ns:UF', nsNFe).text
        cep = endereco.find('ns:CEP', nsNFe).text
        pais = endereco.find('ns:xPais', nsNFe).text
        telefone = endereco.find('ns:fone', nsNFe).text
        
        documento = cpf.text if cpf is not None else cnpj.text
        tipo_documento = 'CPF' if cpf is not None else 'CNPJ'

        endereco_json = {
            'logradouro': logradouro, 'numero': numero, 'bairro': bairro,
            'cidade': cidade, 'estado': estado, 'cep': cep, 'pais': pais, 'telefone': telefone
        }
        
        clientes.append({'nome': xNome, 'documento': documento, 'tipo_documento': tipo_documento, 'endereco': endereco_json})

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
               
                endereco_obj = Endereco.objects.create(logradouro=cliente['endereco']['logradouro'], numero=cliente['endereco']['numero'], bairro=cliente['endereco']['bairro'], cidade=cliente['endereco']['cidade'], estado=cliente['endereco']['estado'], cep=cliente['endereco']['cep'], pais=cliente['endereco']['pais'], telefone=cliente['endereco']['telefone'])
                cliente_obj, created = Cliente.objects.get_or_create(documento=cliente['documento'], defaults={'nome': cliente['nome'], 'tipo_documento': cliente['tipo_documento']}, endereco=endereco_obj)
                nf.clientes.add(cliente_obj)

            for boleto in xml_data['boletos']:
                Boleto.objects.create(valor=boleto['valor'], data_vencimento=boleto['data_vencimento'], nota_fiscal=nf)
          
            return redirect('index')

    return render(request, 'index.html', context)


def list_nfs(request):
    context = {
        'nfs': NotaFiscal.objects.all()
    }
    return render(request, 'list_nfs.html', context)

def detail_nf(request, nf_id):
    context = {
        'nf': NotaFiscal.objects.get(id=nf_id)
    }
    return render(request, 'detail_nf.html', context)

