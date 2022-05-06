from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.infra.settings import settings


if settings.dev == "true":
    if settings.app_docker_run == "true":
        SQLALCHEMY_DATABASE_URL = settings.database_url_docker
    else:
        SQLALCHEMY_DATABASE_URL = settings.database_url

else:
    url = settings.database_url
    if url and url.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = url.replace(
            "postgres://", "postgresql://", 1)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
