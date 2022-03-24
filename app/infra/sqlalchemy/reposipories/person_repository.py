from sqlalchemy.orm import Session

from app.infra.sqlalchemy.models import models
from app.schemas import schemas


def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()


def get_person_by_document(db: Session, cnpj: str, cpf: str):
    if(cnpj):
        return db.query(models.Person).filter(models.Person.cnpj == cnpj).first()
    return db.query(models.Person).filter(models.Person.cpf == cpf).first()


def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()


def create_person(db: Session, person: schemas.PersonCreate):

    db_person = models.Person(**person)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person
