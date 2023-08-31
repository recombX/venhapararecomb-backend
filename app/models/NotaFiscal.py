from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy
from app import db

class NotaFiscal(db.Model):
    __tablename__ = "nfe"
    id = db.Column(db.String(15), primary_key=True, autoincrement="False")
    fornecedor_id = db.Column(db.String(15), ForeignKey("fornecedor.id"), nullable=False)
    cliente_id = db.Column(db.String(15),ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="notas_fiscais")
    fornecedor = relationship("Fornecedor", back_populates="notas_fiscais")

    def add(self):
        db.session.add(self)
    
    def delete(self):
        db.session.delete(self)