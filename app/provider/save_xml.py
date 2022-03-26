from sqlalchemy.orm import Session
import xml.etree.ElementTree as Et
from xml.dom import minidom
from typing import List
from app.infra.sqlalchemy.reposipories import person_repository
from app.infra.sqlalchemy.reposipories import address_repository
from app.infra.sqlalchemy.reposipories import nfe_repository


def get_address(xml, pos) -> dict:
    """Extract information about a person's address (supplier, customer).

    Args:
        xml (str): Is a string from an xml file
        pos (int): This variable indicates which address will be returned.
    Returns:
        dict: Returns a dictionary with information about a person's address.
    """
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


def get_people(xml, pos) -> dict:
    """Extract information about a person (supplier, customer).

    Args:
        xml (str): Is a string from an xml file
        pos (int): this variable indicates which person of the found will be returned.
    Returns:
        dict: Returns a dictionary with information about a person.
    """
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


def get_NFe_info(xml) -> dict:
    """Extract the information regarding the NFe

    Args:
        xml (str): Is a string from an xml file

    Returns:
        dict: Returns a dictionary with information regarding Nfe
    """

    date_venc = xml.getElementsByTagName("dVenc")
    total = xml.getElementsByTagName("vLiq")

    nfe = {
        "date_venc": date_venc[0].firstChild.data,
        "total": total[0].firstChild.data,
    }

    return nfe


def dismember_xml(file: bytes, db: Session) -> None:
    """_summary_

    Args:
        file (bytes): file in binary format
        db (Session): database session
    Returns:
        None
    """
    # convert a binary to string
    xml = Et.fromstring(file)

    # capture the id of the NFe
    for x in xml[0]:
        if x.get('Id'):
            nfe_id = x.get('Id')

    # if the NFe has already been created returns
    if nfe_repository.get_nfe_by_nfe_id(db, nfe_id):
        return

    xml = minidom.parseString(file)

    # capture the information in the NFe by the tags
    enderEmit = get_address(xml, 0)
    enderDest = get_address(xml, 1)

    provider = get_people(xml, 0)
    client = get_people(xml, 1)

    nfe = get_NFe_info(xml)
    nfe['nfe_id'] = nfe_id

    # search for a person by CNPJ and CPF
    db_provider = person_repository.get_person_by_document(
        db, cnpj=provider.get('cnpj'), cpf=provider.get('cpf'))
    db_client = person_repository.get_person_by_document(
        db, cnpj=client.get('cnpj'), cpf=client.get('cpf'))

    # if it doesn't exist create a new person
    if not db_client:
        db_client = person_repository.create_person(db, client)
    # if it doesn't exist create a new person
    if not db_provider:
        db_provider = person_repository.create_person(db, provider)

    if not address_repository.get_address_by_person_id(db, db_provider.id):
        # save the person's address
        address_repository.create_address(
            db, enderEmit, db_provider.id)

    if not address_repository.get_address_by_person_id(db, db_client.id):
        # save the person's address
        address_repository.create_address(
            db, enderDest, db_client.id)

    # create an Nfe

    nfe_repository.create_nfe(db, nfe, db_provider.id, db_client.id)

    return None


async def save_xml(files: List[bytes], db: Session) -> None:
    """_summary_

    Args:
        files (List[bytes]): A list of files in binary format
        db (Session): database session

    Returns:
        None
    """

    for file in files:
        try:
            if(file.decode("utf-8")[:5] == "<?xml"):
                dismember_xml(file.decode("utf-8"), db)
        except Exception:
            return
