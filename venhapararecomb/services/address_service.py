from infra.models import models
from schemas.schemas import AddressCreate
from infra.database import get_db


def create(address: AddressCreate, id_doc):
    db = get_db()
    person = find_by_id(db, id_doc)
    if(not person):
        return
    new_address = models.Address(
        logradouro=address.get('logradouro'),
        numero=address.get('numero'),
        bairro=address.get('bairro'),
        municipio=address.get('municipio'),
        uf=address.get('uf'),
        cep=address.get('cep'),
        pais=address.get('pais'),
        people_id=person.id
    )

    try:
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return new_address
    except Exception:
        return


def find_by_id(id: int):
    db = get_db()
    return db.query(models.Person).filter(models.Person.cnpj == id).first()
