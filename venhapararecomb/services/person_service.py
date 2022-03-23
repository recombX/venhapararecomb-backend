
from sqlalchemy.orm import Session
from infra.models import models
from schemas.schemas import PersonCreate


def create(person: PersonCreate):
    new_person = models.Person(
        name=person.get('name'),
        cpf=person.get('cpf'),
        cnpj=person.get('cnpj'),
        type_person=person.get('type_person')
    )
    try:
        db.add(new_person)
        db.commit()
        db.refresh(new_person)
        return new_person
    except Exception:
        return None


def find_by_cpf(cpf: int):
    return db.query(models.Person).filter(models.Person.cpf == cpf).first()


def find_by_cnpj(cnpj: int):
    return db.query(models.Person).filter(models.Person.cnpj == cnpj).first()
