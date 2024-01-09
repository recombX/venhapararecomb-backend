import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv

def write_csv():
    root = ET.parse("xml/32211207872718000117550010000217781877120005-nfe.xml").getroot()
    nsNFE = {'ns' : "http://www.portalfiscal.inf.br/nfe"}
    
    xml = open("xml/32211207872718000117550010000217781877120005-nfe.xml")
    nfe= minidom.parse(xml)
    
    nome_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFE)
    cnpj_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFE)
    nome_fonec = nome_emit.text
    cnpj_fonec = cnpj_emit.text
    
    nome_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:xNome', nsNFE)
    cnpj_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:CNPJ', nsNFE)
    nome_cli = nome_dest.text
    cnpj_cli = cnpj_dest.text
    
    municipio_cli = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xMun', nsNFE)
    lagradouro_cli = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xLgr', nsNFE)
    bairro_cli = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xBairro', nsNFE)
    numero_cli = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:nro', nsNFE)
    
    endereco = f"municipio: {municipio_cli.text}, lagradouro: {lagradouro_cli.text}, bairro: {bairro_cli.text}, numero: {numero_cli.text}"

    itens = nfe.getElementsByTagName('dup')
    num_dup = 0
    data_venc = ""
    for item in itens:
        num_dup += 1
        try:
            dt_vencimento = item.getElementsByTagName('dVenc')[0].firstChild.data
        except IndexError:
            valor_pis = "Nao consta data"
        data_venc += f"duplicata {num_dup}: {dt_vencimento}; "

    valor_total = nfe.getElementsByTagName('vNF')
    valor = valor_total[0].firstChild.data
    
    
    dados = [
        {"nome_fonec": nome_fonec,"cnpj_fonec": cnpj_fonec,"nome_cli": nome_cli,"cnpj_cli": cnpj_cli,"endereco": endereco,"data_venc": data_venc,"valor": valor},
    ]
    chaves = dados[0].keys()
    
    with open("data.csv", mode='w', newline='') as arquivo_csv:
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=chaves)
        escritor_csv.writeheader()
        
        for linha in dados:
            escritor_csv.writerow(linha)
    return dados

def read_csv():
    with open("data.csv", 'r') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        informacoes = []
        for linha in leitor_csv:
            informacoes.append(linha)
    return informacoes

def test_write_csv():
    result = write_csv()
    expeted = read_csv()
    
    assert result == expeted