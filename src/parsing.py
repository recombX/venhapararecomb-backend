import xml.etree.ElementTree as ET
import re
from models import Fornecedor, Cliente, NotaFiscal
from datetime import datetime

def parse_fornecedor(fornecedor_XML, namespace=''):
    """
    Parses a fornecedor from an XML element.

    Args:
        fornecedor_XML (xml.etree.ElementTree.Element): The XML element to parse.
        namespace (str): The namespace of the XML element.
    
    Returns:
        Fornecedor: The parsed fornecedor.
    """
    if (cnpj := fornecedor_XML.find(f'{namespace}CNPJ')) is not None:
        identificador = cnpj.text
    else:
        identificador = fornecedor_XML.find(f'{namespace}CPF').text

    return Fornecedor(identificador)

def parse_cliente(cliente_XML, namespace=''):
    """"
    Parses a cliente from an XML element.
    
    Args:
        cliente_XML (xml.etree.ElementTree.Element): The XML element to parse.
        namespace (str): The namespace of the XML element.

    Returns:
        Cliente: The parsed cliente.
    """
    if (cnpj := cliente_XML.find(f'{namespace}CNPJ')) is not None:
        identificador = cnpj.text
    else:
        identificador = cliente_XML.find(f'{namespace}CPF').text
    nome = cliente_XML.find(f'{namespace}xNome').text

    endereco_XML = cliente_XML.find(f'{namespace}enderDest')
    logradouro = endereco_XML.find(f'{namespace}xLgr').text
    numero = endereco_XML.find(f'{namespace}nro').text
    municipio = endereco_XML.find(f'{namespace}xMun').text
    unidade_federativa = endereco_XML.find(f'{namespace}UF').text
    endereco = f'{logradouro}, Nº {numero}, {municipio} - {unidade_federativa}'

    return Cliente(identificador, nome, endereco)

def parse_NF(file_content):
    """
    Parses a nota fiscal from an XML file.

    Args:
        file_content (str): The XML file content.

    Returns:
        NotaFiscal: The parsed nota fiscal.
    """
    root_XML = ET.fromstring(file_content)
    NFe_XML = root_XML[0] # NFe
    infNFe_XML = NFe_XML[0] # infNFe
    namespace = regex.group(0) if (regex := re.match(r'\{.*\}', root_XML.tag)) else '' # xmlns

    fornecedor = parse_fornecedor(infNFe_XML.find(f'{namespace}emit'), namespace)
    cliente = parse_cliente(infNFe_XML.find(f'{namespace}dest'), namespace)

    cobranca_XML = infNFe_XML.find(f'{namespace}cobr')
    duplicata_XML = cobranca_XML.findall(f'{namespace}dup')
    boletos = [
        {
            'valor': float(dup_XML.find(f'{namespace}vDup').text), 
            'vencimento': datetime.strptime(dup_XML.find(f'{namespace}dVenc').text, '%Y-%m-%d')
        } 
        for dup_XML in duplicata_XML
    ]

    return NotaFiscal(fornecedor, cliente, boletos)

