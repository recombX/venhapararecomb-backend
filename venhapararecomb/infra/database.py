import databases
import sqlalchemy
import os
from .models.models import create_models

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:123456@localhost:5432/postgres")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

models = create_models(metadata=metadata)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)
