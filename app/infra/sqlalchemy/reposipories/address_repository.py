from sqlalchemy.orm import Session

from app.infra.sqlalchemy.models import models
from app.schemas import schemas


def create_address(db: Session, address: schemas.AddressCreate, id_person):

    db_address = models.Address(**address)
    db_address.person_id = id_person
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address_by_person_id(db: Session, id_person):
    return db.query(models.Address).filter(models.Address.person_id == id_person).first()
