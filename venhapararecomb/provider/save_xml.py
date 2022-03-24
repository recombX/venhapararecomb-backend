from datetime import datetime
import shutil
import os
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET


def get_address(xml, pos):
    logradouro = xml.getElementsByTagName("xLgr")
    numero = xml.getElementsByTagName("nro")
    bairro = xml.getElementsByTagName("xBairro")
    municipio = xml.getElementsByTagName("xMun")
    uf = xml.getElementsByTagName("UF")
    cep = xml.getElementsByTagName("CEP")
    pais = xml.getElementsByTagName("xPais")
    address = {
        "logradouro": logradouro[pos].firstChild.data,
        "numero": numero[pos].firstChild.data,
        "bairro": bairro[pos].firstChild.data,
        "municipio": municipio[pos].firstChild.data,
        "uf": uf[pos].firstChild.data,
        "cep": cep[pos].firstChild.data,
        "pais": pais[pos].firstChild.data,
    }
    return address


def get_people(xml, pos):

    name = xml.getElementsByTagName("xNome")
    cpf = xml.getElementsByTagName("CPF")
    cnpj = xml.getElementsByTagName("CNPJ")
    person = {
        "name": name[pos].firstChild.data,
        "type_person": pos
    }
    if(cpf == []):
        person['cpf'] = None
    else:
        person['cpf'] = cpf[pos].firstChild.data

    if(cnpj == []):
        person['cnpj'] = None
    else:
        person['cnpj'] = cnpj[pos].firstChild.data

    return person


def get_NFe_info(xml):
    date_venc = xml.getElementsByTagName("dVenc")
    total = xml.getElementsByTagName("vLiq")

    nfe = {
        "date_venc": date_venc[0].firstChild.data,
        "total": total[0].firstChild.data,
    }
    return nfe


def dismember_xml(path):
    with open(path, "r", encoding='utf-8') as f:
        xml = parse(f)
        tree = ET.parse(path)
        root = tree.getroot()

        for child in root[0]:
            if('Id' in child.attrib):
                nfe_id = child.attrib['Id']
    os.remove(path)
    enderEmit = get_address(xml, 0)
    enderDest = get_address(xml, 1)

    provider = get_people(xml, 0)
    client = get_people(xml, 1)

    nfe = get_NFe_info(xml)
    nfe["nfe_id"] = nfe_id

    data = {
        "enderEmit": enderEmit,
        "enderDest": enderDest,
        "provider": provider,
        "client": client,
        "nfe": nfe,
    }


async def save_xml(files):
    for file in files:
        if file.filename[-3:] == 'xml':
            timestamp = datetime.timestamp(datetime.now())
            filename = f'{timestamp}-{file.filename}'
            path = f"./venhapararecomb/static/xmlDocs/{filename}"
            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            dismember_xml(path)
