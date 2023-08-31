from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db
from app.models.NotaFiscal import NotaFiscal

class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.String(15), primary_key=True, autoincrement="False")
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    cep = db.Column(db.String(8))


    notas_fiscais = relationship("NotaFiscal", back_populates="cliente")

    def add(self):
        db.session.add(self)
    
    def delete(self):
        db.session.delete(self)


