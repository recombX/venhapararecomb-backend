from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .models import Fornecedor, Cliente, Boleto, NotaFiscal, Endereco
from django.urls import reverse
from django.views.decorators.http import require_POST


def parse_xml(xml_file):
    """
    Esta função recebe um arquivo XML e extrai informações relevantes para o sistema de notas fiscais.

    Args:
        xml_file: O arquivo XML enviado pelo usuário.

    Returns:
        dict: Um dicionário contendo informações extraídas do XML, incluindo ID da nota fiscal, fornecedor,
              clientes e boletos.
    """

    xml = ET.parse(xml_file)
    root = xml.getroot()
    nsNFe = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    nf_id = root.find('.//ns:infNFe', nsNFe).attrib['Id']

    # Extraindo informações do fornecedor da nota fiscal (emitente)
    xNome = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe).text
    cnpj = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe).text
    fornecedor = {'nome': xNome, 'cnpj': cnpj}
   
    # Extraindo informações dos clientes da nota fiscal
    clientes = []
    for dest in root.findall('ns:NFe/ns:infNFe/ns:dest', nsNFe):
        xNome = dest.find('ns:xNome', nsNFe).text
        cpf = dest.find('ns:CPF', nsNFe)
        cnpj = dest.find('ns:CNPJ', nsNFe)

        # Extraindo informações do endereço do cliente
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

    # Extraindo informações dos boletos da nota fiscal
    boletos = []
    for det in root.findall('ns:NFe/ns:infNFe/ns:cobr/ns:dup', nsNFe):
        valor = det.find('ns:vDup', nsNFe).text
        data_vencimento = det.find('ns:dVenc', nsNFe).text
        boletos.append({'valor': valor, 'data_vencimento': data_vencimento}) # Adicionando informações do boleto à lista de boletos 

    return {'nf_id': nf_id, 'fornecedor': fornecedor, 'clientes': clientes, 'boletos': boletos}



def index(request):
    """
    Esta função é responsável por renderizar a página inicial do sistema de notas fiscais.
    Permite aos usuários enviar arquivos XML para processamento e salvar as informações da nota fiscal no banco de dados.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com base na solicitação do usuário.
    """
    context = {}
    if request.method == 'POST':
        # Verificando se o usuário deseja ler um arquivo XML
        if 'read_xml' in request.POST:
            xml_data = parse_xml(request.FILES['xml_file'])
            request.session['xml_data'] = xml_data
            context['xml_data'] = xml_data

        # Verificando se o usuário deseja salvar a nota fiscal lida
        elif 'save_nf' in request.POST:
            xml_data = request.session.pop('xml_data', {})
            fornecedor, _ = Fornecedor.objects.get_or_create(nome=xml_data['fornecedor']['nome'], cnpj=xml_data['fornecedor']['cnpj'])
            nf, created = NotaFiscal.objects.get_or_create(identificador=xml_data['nf_id'], fornecedor=fornecedor)
            
            # Verificando se a nota fiscal já foi cadastrada
            if not created:
                context['error'] = 'Nota Fiscal já cadastrada'
                context['xml_data'] = xml_data
                return render(request, 'index.html', context)

            # Adicionando clientes à nota fiscal
            for cliente_data in xml_data['clientes']:
                documento = cliente_data['documento']
                try:
                    cliente_obj = Cliente.objects.get(documento=documento)
                except Cliente.DoesNotExist:
                    endereco_obj = Endereco.objects.create(**cliente_data['endereco'])
                    cliente_obj = Cliente.objects.create(documento=documento, nome=cliente_data['nome'], tipo_documento=cliente_data['tipo_documento'], endereco=endereco_obj)
                
                nf.clientes.add(cliente_obj)

            # Adicionando boletos à nota fiscal
            for boleto_data in xml_data['boletos']:
                Boleto.objects.create(valor=boleto_data['valor'], data_vencimento=boleto_data['data_vencimento'], nota_fiscal=nf)

            context['success'] = 'Nota Fiscal cadastrada com sucesso'

    return render(request, 'index.html', context)

@require_POST
def delete_nf(request, id):
    """
    Esta função é responsável por deletar uma nota fiscal do banco de dados.

    Args:
        id: O ID da nota fiscal a ser deletada.

    Returns:
        HttpResponseRedirect: Redireciona o usuário para a página de listagem de notas fiscais após a exclusão.
    """
    try:
        nf = NotaFiscal.objects.get(id=id)
        nf.delete()
    except NotaFiscal.DoesNotExist:
        pass
    return redirect(reverse('list_nfs'))


def list_nfs(request):
    """
    Esta função é responsável por listar todas as notas fiscais cadastradas no sistema.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com base na solicitação do usuário, listando todas as notas fiscais.
    """
    context = {
        'nfs': NotaFiscal.objects.all()
    }
    return render(request, 'list_nfs.html', context)


def detail_nf(request, id):
    """
    Esta função é responsável por renderizar a página de detalhes de uma nota fiscal.

    Args:
        id: O ID da nota fiscal a ser visualizada.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com base na solicitação do usuário, exibindo os detalhes da nota fiscal.
    """
    
    nf =  NotaFiscal.objects.get(id=id)
    clientes = nf.clientes.all()
    fornecedor = nf.fornecedor
    boletos = Boleto.objects.filter(nota_fiscal=nf)

    context = {
        'nf': nf,
        'clientes': clientes,
        'boletos': boletos,
        'fornecedor': fornecedor
    }

    return render(request, 'detail_nf.html', context)

@require_POST
def delete_fornecedor(request, id):
    """
    Esta função é responsável por deletar um fornecedor do banco de dados.

    Args:
        id: O ID do fornecedor a ser deletado.

    Returns:
        HttpResponseRedirect: Redireciona o usuário para a página de listagem de fornecedores após a exclusão.
    """
    try:
        fornecedor = Fornecedor.objects.get(id=id)
        fornecedor.delete()
    except Fornecedor.DoesNotExist:
        pass
    return redirect(reverse('list_fornecedores'))

def list_fornecedores(request):
    """
    Esta função é responsável por listar todos os fornecedores cadastrados no sistema.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com base na solicitação do usuário, listando todos os fornecedores.
    """
    context = {
        'fornecedores': Fornecedor.objects.all()
    }
    return render(request, 'list_fornecedores.html', context)

@require_POST
def delete_cliente(request, id):
    """
    Esta função é responsável por deletar um cliente do banco de dados.

    Args:
        id: O ID do cliente a ser deletado.

    Returns:
        HttpResponseRedirect: Redireciona o usuário para a página de listagem de clientes após a exclusão.
    """
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
    except Cliente.DoesNotExist:
        pass
    return redirect(reverse('list_clientes'))

def list_clientes(request):
    """
    Esta função é responsável por listar todos os clientes cadastrados no sistema.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com base na solicitação do usuário, listando todos os clientes.
    """
    context = {
        'clientes': Cliente.objects.all()
    }
    
    return render(request, 'list_clientes.html', context)


