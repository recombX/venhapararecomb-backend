
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf = Column(String, nullable=True, unique=True)
    cnpj = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    address = relationship("Address", back_populates='person')


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
    person_id = Column(Integer, ForeignKey(
        'person.id'), name='fk_person_address')

    person = relationship("Person", back_populates='address')


class NFe(Base):
    __tablename__ = "nfe"

    id = Column(Integer, primary_key=True, index=True)
    nfe_id = Column(String, nullable=False, unique=True)
    date_venc = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    provider_id = Column(Integer, ForeignKey('person.id'),
                         name='fk_person_provider_nfe')
    client_id = Column(Integer, ForeignKey('person.id'),
                       name='fk_person_client_nfe')
