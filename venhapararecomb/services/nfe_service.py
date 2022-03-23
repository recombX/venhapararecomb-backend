
from infra.models import models
from schemas.schemas import NfeCreate


def create(nfe: NfeCreate, id_person):

    if(find_by_id(db, nfe.provider_id)):
        return
    if(find_by_id(db, nfe.client_id)):
        return
    new_nfe = models.NFe(
        nfe_id=nfe.nfe_id,
        date_venc=nfe.date_venc,
        total=nfe.total,
        provider_id=nfe.provider_id,
        client_id=nfe.client_id
    )

    try:
        db.add(new_nfe)
        db.commit()
        db.refresh(new_nfe)
        return new_nfe
    except Exception:
        return


def find_by_id(id: int):
    return db.query(models.Person).filter(models.Person.id == id).first()
