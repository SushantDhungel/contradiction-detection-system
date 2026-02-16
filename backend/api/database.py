from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends
from configs import Config
from typing import Annotated

# Import all models so they are registered with SQLModel.metadata
from models import Document

config = Config()

engine = create_engine(config.get_sync_db_url())


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

init_db()