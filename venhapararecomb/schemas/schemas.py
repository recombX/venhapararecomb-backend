from datetime import datetime
from pydantic import BaseModel


class PersonCreate(BaseModel):
    name: str
    cpf: str | None = None
    cnpj: str | None = None
    type_person: int

    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    logradouro: str | None = None
    numero: int | None = None
    bairro: str | None = None
    municipio: str | None = None
    uf: str | None = None
    cep: str | None = None
    pais: str | None = None


class NfeCreate(BaseModel):
    nfe_id: str
    date_venc: datetime
    total: float
    provider_id: int
    client_id: int
