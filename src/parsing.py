import xml.etree.ElementTree as ET
import re
from models import Fornecedor, Cliente, NotaFiscal
from datetime import datetime

def parse_fornecedor(fornecedor_xml, namespace=''):
    """
    Parses a fornecedor from an XML element.

    Args:
        fornecedor_xml (xml.etree.ElementTree.Element): The XML element to parse.
        namespace (str): The namespace of the XML element.
    
    Returns:
        Fornecedor: The parsed fornecedor.
    """
    if (cnpj := fornecedor_xml.find(f'{namespace}CNPJ')) is not None:
        identificador = cnpj.text
    else:
        identificador = fornecedor_xml.find(f'{namespace}CPF').text

    return Fornecedor(identificador)

def parse_cliente(cliente_xml, namespace=''):
    """"
    Parses a cliente from an XML element.
    
    Args:
        cliente_xml (xml.etree.ElementTree.Element): The XML element to parse.
        namespace (str): The namespace of the XML element.

    Returns:
        Cliente: The parsed cliente.
    """
    if (cnpj := cliente_xml.find(f'{namespace}CNPJ')) is not None:
        identificador = cnpj.text
    else:
        identificador = cliente_xml.find(f'{namespace}CPF').text
    nome = cliente_xml.find(f'{namespace}xNome').text

    endereco_xml = cliente_xml.find(f'{namespace}enderDest')
    logradouro = endereco_xml.find(f'{namespace}xLgr').text
    numero = endereco_xml.find(f'{namespace}nro').text
    municipio = endereco_xml.find(f'{namespace}xMun').text
    unidade_federativa = endereco_xml.find(f'{namespace}UF').text
    endereco = f'{logradouro}, Nº {numero}, {municipio} - {unidade_federativa}'

    return Cliente(identificador, nome, endereco)

def parse_nota_fiscal(file_content):
    """
    Parses a nota fiscal from an XML file.

    Args:
        file_content (str): The XML file content.

    Returns:
        NotaFiscal/None: The parsed nota fiscal or None if the file is not a nota fiscal.
    """
    try:
        root_xml = ET.fromstring(file_content)
        nfe_xml = root_xml[0] # NFe
        inf_nfe_xml = nfe_xml[0] # infNFe
        namespace = regex.group(0) if (regex := re.match(r'\{.*\}', root_xml.tag)) else '' # xmlns

        fornecedor = parse_fornecedor(inf_nfe_xml.find(f'{namespace}emit'), namespace)
        cliente = parse_cliente(inf_nfe_xml.find(f'{namespace}dest'), namespace)

        cobranca_xml = inf_nfe_xml.find(f'{namespace}cobr')
        duplicata_xml = cobranca_xml.findall(f'{namespace}dup')
        boletos = [
            {
                'valor': float(dup_xml.find(f'{namespace}vDup').text), 
                'vencimento': datetime.strptime(dup_xml.find(f'{namespace}dVenc').text, '%Y-%m-%d')
            } 
            for dup_xml in duplicata_xml
        ]

        return NotaFiscal(inf_nfe_xml.attrib['Id'][3:], fornecedor, cliente, boletos)

    except Exception:
        return None

