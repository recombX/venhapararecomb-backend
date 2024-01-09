import xml.etree.ElementTree as ET
from xml.dom import minidom


def BuscarDadosEmissor(caminho_arquivo) -> list:
    root = ET.parse(caminho_arquivo).getroot()
    nsNFE = {'ns' : "http://www.portalfiscal.inf.br/nfe"}
    
    cnpj_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFE)
    nome_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFE)
    
    emit = ["CNPJ: "+cnpj_emit.text,"Nome: "+nome_emit.text]
    return emit


def BuscarEnderecoEmissor(caminho_arquivo) -> list:
    root = ET.parse(caminho_arquivo).getroot()
    nsNFE = {'ns' : "http://www.portalfiscal.inf.br/nfe"}
    
    end_lgr_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xLgr', nsNFE)
    end_numero_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:nro', nsNFE)
    end_complemento_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xCpl', nsNFE)
    end_bairro_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xBairro', nsNFE)
    end_municipio_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xMun', nsNFE)
    end_cod_municipio_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:cMun', nsNFE)
    end_estado_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:UF', nsNFE)
    end_CEP_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:CEP', nsNFE)
    end_cod_pais_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:cPais', nsNFE)
    end_pais_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:xPais', nsNFE)
    end_fone_emit = root.find('ns:NFe/ns:infNFe/ns:emit/ns:enderEmit/ns:fone', nsNFE)
    
    endereco = [
        "Lagradouro: "+end_lgr_emit.text,
        "Numero: "+end_numero_emit.text,
        "Bairro: "+end_bairro_emit.text,
        "Municipio: "+end_municipio_emit.text,
        "Codigo municipio: "+end_cod_municipio_emit.text,
        "UF: "+end_estado_emit.text,
        "CEP: "+end_CEP_emit.text,
        "Codigo pais: "+end_cod_pais_emit.text,
        "Pais: "+end_pais_emit.text,
        "Telefone: "+end_fone_emit.text 
    ]
    return endereco
    
    
    
def BuscarDadosDestinatario(caminho_arquivo) -> list:
    root = ET.parse(caminho_arquivo).getroot()
    nsNFE = {'ns' : "http://www.portalfiscal.inf.br/nfe"}
        
    cnpj_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:CNPJ', nsNFE)
    nome_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:xNome', nsNFE)
    
    dest = ["CNPJ: "+ cnpj_dest.text,"Nome: "+nome_dest.text]   
    return dest
 
    
def BuscarEnderecoDestinatario(caminho_arquivo) -> list:
    root = ET.parse(caminho_arquivo).getroot()
    nsNFE = {'ns' : "http://www.portalfiscal.inf.br/nfe"}
    
    end_lgr_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xLgr', nsNFE)
    end_numero_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:nro', nsNFE)
    end_bairro_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xBairro', nsNFE)
    end_municipio_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xMun', nsNFE)
    end_cod_municipio_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:cMun', nsNFE)
    end_estado_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:UF', nsNFE)
    end_CEP_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:CEP', nsNFE)
    end_cod_pais_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:cPais', nsNFE)
    end_pais_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xPais', nsNFE)
    end_fone_dest = root.find('ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:fone', nsNFE)
    
    endereco = [
        "Lagradouro: "+end_lgr_dest.text,
        "Numero: "+end_numero_dest.text,
        "Bairro: "+end_bairro_dest.text,
        "Municipio: "+end_municipio_dest.text,
        "Codigo municipio: "+end_cod_municipio_dest.text,
        "UF: "+end_estado_dest.text,
        "CEP: "+end_CEP_dest.text,
        "Codigo pais: "+end_cod_pais_dest.text,
        "Pais: "+end_pais_dest.text,
        "Telefone: "+end_fone_dest.text 
    ]
    return endereco
  
   
    
def BuscarValorItens(caminho_arquivo) -> list:
    xml = open(caminho_arquivo)
    nfe= minidom.parse(xml)
    itens = nfe.getElementsByTagName('det')
    valores = []
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
        #impostos
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
        
        valor = [
            "Item " + num_item,
            "Valor: " + valor_item,
            "Valor unidade: " + valor_uniProd,
            "Impostos ICMS: " + valor_icms,
            "Impostos PIS: " + valor_pis,
            "Impostos CONFINS: " + valor_cofins
        ]
        valores += valor
    return valores
        

def BuscarDataVencimento(caminho_arquivo)->list:
    
    xml = open(caminho_arquivo)
    nfe= minidom.parse(xml)
        
    itens = nfe.getElementsByTagName('dup')
    num_dup = 0
    datas = []
    for item in itens:
        num_dup += 1
        try:
            dt_vencimento = item.getElementsByTagName('dVenc')[0].firstChild.data
        except IndexError:
            valor_pis = "Nao consta data"
        data = [num_dup,dt_vencimento]
        datas += data       
    return datas
    

def BuscarvalorPagar(caminho_arquivo)->list:
    xml = open(caminho_arquivo)
    nfe= minidom.parse(xml)
    valor_orig = nfe.getElementsByTagName('vOrig')
    valor_desc = nfe.getElementsByTagName('vDesc')
    valor_total = nfe.getElementsByTagName('vNF')
    
    
    valores = [
        "Valor original: "+valor_orig[0].firstChild.data,
        "Desconto: "+valor_desc[0].firstChild.data,
        "Total: "+valor_total[0].firstChild.data
    ]
    return valores
    
