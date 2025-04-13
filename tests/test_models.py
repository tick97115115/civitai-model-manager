import pytest
pytestmark = pytest.mark.anyio

from src.civitai_model_manager.app.db.civitai_table import ModelVersionImage, Model_Id, Model_Tag, ModelVersion, ModelVersionFile

from pathlib import Path
from sqlalchemy import Column
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship, JSON
import os
import json

from src.civitai_model_manager.app.data_model import CivitAI_ModelId


@pytest.fixture(name="session")
def get_db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def model_id_data_list():
    with open(Path(__file__).parent / 'modeid_data_list.json', mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())
        return [CivitAI_ModelId(**obj) for obj in data]


def test_sql_model_instantiation(model_id_data_list, session: Session):
    model_id = model_id_data_list[0]
    model_id_ = Model_Id(
        id=model_id.id,
        name=model_id.name,
        type=model_id.type,
        nsfw=model_id.nsfw,
        nsfw_level=model_id.nsfwLevel,
        api_info_model_id=model_id.model_dump(),
        model_versions=[]
        # model_versions=[ModelVersion(
        #     id=model_version.id,
        #     name=model_version.name,
        #     base_model=model_version.baseModel,
        #     nsfw_level=model_version.nsfwLevel,
        #     model_id=model_id.id,
        #     api_info_model_version=model_version.model_dump(),
        #     images=[],
        #     files=[]
        # ) for model_version in model_id.modelVersions],
        tags=[Model_Tag(name=tag) for tag in model_id.tags]
    )
    for model_version in model_id.modelVersions:
        

    # for model_version_ in model_id_.model_versions:
    #     model_version_.model = model_id_
    #     model_version_.files=[ModelVersionFile(
    #         id=file.id,
    #         size_kb=file.size_kb,
    #         name=file.name,
    #         type=file.type,
    #         download_url=file.download_url,
    #         api_info_file=file.model_dump(),
    #         model_version_id=model_version_.id,
    #         model_version=model_version_
    #     ) for file in model_version_.files]
    #     model_version_.images=[ModelVersionImage(
    #         id=image.id,
    #         url=image.url,
    #         nsfw_level=image.nsfw_level,
    #         image_data=b'test',
    #         api_info_image=image.model_dump(),
    #         model_version_id=model_version_.id,
    #         model_version=model_version_
    #     ) for image in model_version_.images]
    session.add(model_id_)
    session.commit()
    session.refresh(model_id_)
    
    assert model_id_data_list