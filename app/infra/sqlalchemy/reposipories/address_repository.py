from sqlalchemy.orm import Session


class AddressRepository():

    def __init__(self, db: Session):
        self.db = db

    def create(self):
        pass

    def list_all(self):
        pass

    def list_by_id(self):
        pass
