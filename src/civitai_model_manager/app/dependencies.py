from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
from typing import Annotated

from civitai_model_manager.startup import settings
from .db.civitai_table import CivitAI_ModelId
from .db.gopeed_table import ModelVersionGopeedTask

engine = create_engine(settings.db_uri)
SQLModel.metadata.create_all(engine)

@contextmanager
def get_db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

DbSessionDep = Annotated[Session, Depends(get_db_session)]

