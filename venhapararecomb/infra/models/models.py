from sqlalchemy.sql import func
import sqlalchemy


def create_models(metadata):

    person = sqlalchemy.Table(
        "person",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("cpf", sqlalchemy.String,
                          nullable=True, unique=True),
        sqlalchemy.Column("cnpj", sqlalchemy.String,
                          nullable=True, unique=True),
        sqlalchemy.Column("type_person", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True),
                          server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True),
                          server_default=func.now(), onupdate=func.now()),
    )

    address = sqlalchemy.Table(
        "address",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("logradouro", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("numero", sqlalchemy.String, nullable=True),
        sqlalchemy.Column("bairro", sqlalchemy.String, nullable=True),
        sqlalchemy.Column("municipio", sqlalchemy.String, nullable=True),
        sqlalchemy.Column("uf", sqlalchemy.String, nullable=True),
        sqlalchemy.Column("cep", sqlalchemy.String, nullable=True),
        sqlalchemy.Column("pais", sqlalchemy.String, nullable=True),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True),
                          server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True),
                          server_default=func.now(), onupdate=func.now()),
        sqlalchemy.Column('person_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('person.id', ondelete="CASCADE"))
    )

    nfe = sqlalchemy.Table(
        "nfe",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("nfe_id", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("date_venc", sqlalchemy.DateTime),
        sqlalchemy.Column("total", sqlalchemy.DECIMAL),
        sqlalchemy.Column("type_person", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True),
                          server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True),
                          server_default=func.now(), onupdate=func.now()),

        sqlalchemy.Column('provider_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('person.id', ondelete="CASCADE")),
        sqlalchemy.Column('client_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('person.id', ondelete="CASCADE"))
    )
    return {
        "person": person,
        "address": address,
        "nfe": nfe
    }
