from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os


env = os.getenv("DEV", "true")

if env == "true":
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/postgres"
else:
    url = os.getenv(
        "DATABASE_URL", "postgresql://postgres:123456@localhost:5432/postgres")
    if url and url.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = url.replace(
            "postgres://", "postgresql://", 1)
print(env)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
