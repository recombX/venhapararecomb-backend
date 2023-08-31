from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db
from app.models.NotaFiscal import NotaFiscal

class Fornecedor(db.Model):
    __tablename__ = "fornecedor"
    id = db.Column(db.String(15), primary_key=True, autoincrement="False")
    nome = db.Column(db.String(100), nullable=False)

    notas_fiscais = relationship("NotaFiscal", back_populates="fornecedor")

    def add(self):
        db.session.add(self)
    
    def delete(self):
        db.session.delete(self)

