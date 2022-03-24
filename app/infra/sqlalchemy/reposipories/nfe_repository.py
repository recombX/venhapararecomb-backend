from sqlalchemy.orm import Session

from app.infra.sqlalchemy.models import models
from app.schemas import schemas


def create_nfe(db: Session, nfe: schemas.NfeCreate, provider_id: int, client_id: int):

    db_nfe = models.NFe(**nfe)
    db_nfe.client_id = client_id
    db_nfe.provider_id = provider_id
    db.add(db_nfe)
    db.commit()
    db.refresh(db_nfe)
    return db_nfe


def get_nfe_by_provider_id(db: Session, provider_id: int):
    return db.query(models.NFe).filter(models.NFe.provider_id == provider_id).first()


def get_nfe_by_client_id(db: Session, client_id: int):
    return db.query(models.NFe).filter(models.NFe.client_id == client_id).first()


def get_nfe_by_nfe_id(db: Session, nfe_id: str):
    return db.query(models.NFe).filter(models.NFe.nfe_id == nfe_id).first()


def get_all_nfe(db: Session):
    return db.query(models.NFe).all()
