import xml.etree.ElementTree as Et
from xml.dom import minidom
from sqlalchemy.orm import Session
from app.infra.sqlalchemy.reposipories import person_repository
from app.infra.sqlalchemy.reposipories import address_repository
from app.infra.sqlalchemy.reposipories import nfe_repository
from fastapi import HTTPException, status


def get_address(file, pos):
    xml = minidom.parseString(file)
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


def get_people(file, pos):
    xml = minidom.parseString(file)
    name = xml.getElementsByTagName("xNome")
    cpf = xml.getElementsByTagName("CPF")
    cnpj = xml.getElementsByTagName("CNPJ")
    person = {
        "name": name[pos].firstChild.data
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


def get_NFe_info(file):
    xml = minidom.parseString(file)
    date_venc = xml.getElementsByTagName("dVenc")
    total = xml.getElementsByTagName("vLiq")

    nfe = {
        "date_venc": date_venc[0].firstChild.data,
        "total": total[0].firstChild.data,
    }

    return nfe


def dismember_xml(file, db: Session):
    xml = Et.fromstring(file)
    for x in xml[0]:
        if x.get('Id'):
            nfe_id = x.get('Id')

    enderEmit = get_address(file, 0)
    enderDest = get_address(file, 1)

    provider = get_people(file, 0)
    client = get_people(file, 1)

    nfe = get_NFe_info(file)
    nfe['nfe_id'] = nfe_id

    db_provider = person_repository.get_person_by_document(
        db, cnpj=provider.get('cnpj'), cpf=provider.get('cpf'))
    db_client = person_repository.get_person_by_document(
        db, cnpj=client.get('cnpj'), cpf=client.get('cpf'))

    if not db_client:
        db_client = person_repository.create_person(db, client)

    if not db_provider:
        db_provider = person_repository.create_person(db, provider)

    if not address_repository.get_address_by_person_id(db, db_provider.id):
        address_repository.create_address(
            db, enderEmit, db_provider.id)

    if not address_repository.get_address_by_person_id(db, db_client.id):
        address_repository.create_address(
            db, enderDest, db_client.id)

    if not nfe_repository.get_nfe_by_nfe_id(db, nfe_id):
        nfe_repository.create_nfe(db, nfe, db_provider.id, db_client.id)

    data = {
        "nfe": nfe,
        "provedor": provider,
        "client": client,
        "origem": enderEmit,
        "destino": enderDest,
    }
    return data


async def save_xml(files, db: Session):
    nfe_lst = []
    for file in files:
        try:
            if(file.decode("utf-8")[:5] == "<?xml"):
                nfe_lst.append(dismember_xml(file.decode("utf-8"), db))
        except Exception:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "this document does not exist."}
            )
    return nfe_lst
