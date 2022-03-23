from ..database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

PROVAIDER = 1
CLIENT = 2


class Person(Base):

    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)
    type_person = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    def __str__(self) -> str:
        return f'name: {self.name}'


class Provaider(Person):
    pass


class Client(Person):
    address = relationship("Adress", back_populates="people")


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    logradouro = Column(String, nullable=True)
    numero = Column(Integer, nullable=True)
    bairro = Column(String, nullable=True)
    municipio = Column(String, nullable=True)
    uf = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    pais = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    enterprise_id = Column(Integer, ForeignKey("people.id"))
    enterprise = relationship("Person", back_populates="address")

    def __str__(self) -> str:
        return f'Address: {self.uf} - {self.municipio}'


class NFe(Base):

    __tablename__ = "nfe"

    id = Column(Integer, primary_key=True, index=True)
    nfe_id = Column(String)
    date_venc = Column(DateTime(timezone=True))
    total = Column(DECIMAL, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    provider_id = Column(Integer, ForeignKey("people.id"))
    provider = relationship("Person", back_populates="nfe")

    client_id = Column(Integer, ForeignKey("people.id"))
    client = relationship("Person", back_populates="nfe")

    def __str__(self) -> str:
        return f'NFe: {self.nfeid}'
