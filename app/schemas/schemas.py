from datetime import datetime
from pydantic import BaseModel


class PersonCreate(BaseModel):
    """
    schema of creating a person in the database
    """
    name: str
    cpf: str | None = None
    cnpj: str | None = None

    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    """
    schema of creating a person in the database
    """
    logradouro: str | None = None
    numero: int | None = None
    bairro: str | None = None
    municipio: str | None = None
    uf: str | None = None
    cep: str | None = None
    pais: str | None = None

    class Config:
        orm_mode = True


class AddressView(BaseModel):
    """route response schema
    """
    id: int
    logradouro: str | None = None
    numero: int | None = None
    bairro: str | None = None
    municipio: str | None = None
    uf: str | None = None
    cep: str | None = None
    pais: str | None = None


class PersonView(BaseModel):
    """route response schema
    """
    id: int
    name: str
    cpf: str | None = None
    cnpj: str | None = None
    address: AddressView


class NFeView(BaseModel):
    """route response schema
    """

    id: int
    nfe_id: str
    date_venc: datetime
    total: float
    provider: PersonView
    client: PersonView


class NfeCreate(BaseModel):
    """
    schema of creating a person in the database
    """
    nfe_id: str
    date_venc: datetime
    total: float
    provider_id: int
    client_id: int

    class Config:
        orm_mode = True
