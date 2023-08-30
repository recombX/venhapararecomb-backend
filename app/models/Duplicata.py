from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app import db

class Duplicata(db.Model):
    __tablename__ = "duplicata"
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float(), nullable=False)
    dataVencimento = db.Column(db.Date(), nullable=False)
    nfe = db.Column(ForeignKey("nfe.id"))

    def add(self):
        db.session.add(self)
    
    def delete(self):
        db.session.delete(self)



