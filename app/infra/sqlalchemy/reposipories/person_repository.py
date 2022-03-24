from sqlalchemy.orm import Session
from app.schemas.schemas import PersonCreate
from ..models.models import Person


class PersonRepository():

    def __init__(self, db: Session):
        self.db = db

    def create(self, person: PersonCreate):

        db_person = Person(**person)

        self.db.add(db_person)
        self.db.commit()
        self.db.refresh(db_person)

        return db_person

    def list_all(self):
        pass

    def list_by_id(self):
        pass
