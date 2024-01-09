import xml.etree.ElementTree as ET
from xml.dom import minidom


def test_buscar_dados_emissor():
    tree = ET.parse("xml/32211207872718000117550010000217781877120005-nfe.xml")
    root = tree.getroot()
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    
    cnpj_emit = root.find('.//ns:emit/ns:CNPJ', ns)
    nome_emit = root.find('.//ns:emit/ns:xNome', ns)
    
    result = [cnpj_emit.text, nome_emit.text]
    expected = ["07872718000117", "COMERCIAL S.R.DE ALIMENTOS LTDA-ME"]
    
    assert result == expected



def test_buscar_dados_destinatario():
    tree = ET.parse("xml/32211207872718000117550010000217781877120005-nfe.xml")
    root = tree.getroot()
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    
    cnpj_dest = root.find('.//ns:dest/ns:CNPJ', ns)
    nome_dest = root.find('.//ns:dest/ns:xNome', ns)
    
    result = [cnpj_dest.text, nome_dest.text]
    expected = ["17197072000173", "JEFERSON SIMAO DE OLIVEIRA - ME"]
    
    assert result == expected
    
    

def test_Buscar_valor_itens():
    xml = open("xml/32211207872718000117550010000217781877120005-nfe.xml")
    nfe = minidom.parse(xml)
    itens = nfe.getElementsByTagName('det')
    results = []
    for item in itens:
        num_item = item.getAttribute('nItem')
        try:
            valor_item = item.getElementsByTagName('vProd')[0].firstChild.data
        except IndexError:
            valor_item = "N/A"
        try:
            valor_uniProd = item.getElementsByTagName('vUnTrib')[0].firstChild.data
        except IndexError:
            valor_uniProd = "N/A"
        try:
            valor_icms = item.getElementsByTagName('vICMS')[0].firstChild.data  
        except IndexError:
            valor_icms = "N/A"
        try:
            valor_pis = item.getElementsByTagName('vPIS')[0].firstChild.data  
        except IndexError:
            valor_pis = "N/A"
        try:
            valor_cofins = item.getElementsByTagName('vCOFINS')[0].firstChild.data 
        except IndexError:
            valor_cofins = "N/A"
        
        results.append({
            "num_item": num_item,
            "valor_item": valor_item,
            "valor_uniProd": valor_uniProd,
            "valor_icms": valor_icms,
            "valor_pis": valor_pis,
            "valor_cofins": valor_cofins
        })

    expected = [
        {
            "num_item": "1",
            "valor_item": "503.82",
            "valor_uniProd": "27.99",
            "valor_icms": "35.27",
            "valor_pis": "3.27",
            "valor_cofins": "15.11"
        },
        
        {
            "num_item": "2",
            "valor_item": "632.41",
            "valor_uniProd": "29.12989406",
            "valor_icms": "N/A",
            "valor_pis": "4.11",
            "valor_cofins": "18.97"
            
        }
    ]

    assert len(results) == len(expected)
    
def test_buscar_data_vencimento():   
    xml = open("xml/32211207872718000117550010000217781877120005-nfe.xml")
    nfe= minidom.parse(xml)
        
    itens = nfe.getElementsByTagName('dup')
    num_dup = 0
    results = []
    for item in itens:
        num_dup += 1
        try:
            dt_vencimento = item.getElementsByTagName('dVenc')[0].firstChild.data
        except IndexError:
            valor_pis = "Nao consta data"
        results.append(dt_vencimento)
        
    expected = ["2022-12-15","2022-12-22"]
    
    assert results == expected
    

def test_buscar_valor_pagar():
    xml = open("xml/32211207872718000117550010000217781877120005-nfe.xml")
    nfe= minidom.parse(xml)
    valor_orig = nfe.getElementsByTagName('vOrig')
    valor_desc = nfe.getElementsByTagName('vDesc')
    valor_total = nfe.getElementsByTagName('vNF')
    
    results = [valor_orig[0].firstChild.data, valor_desc[0].firstChild.data,valor_total[0].firstChild.data]
    expected = ["1136.23","0.00","1136.23"]
    
    assert results == expected