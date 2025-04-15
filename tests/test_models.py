import pytest
pytestmark = pytest.mark.anyio

from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship, JSON
import json
from src.civitai_model_manager.app.db.civitai_table import Model_Id, ModelVersionImage, Model_Tag, ModelVersion, ModelVersionFile
from src.civitai_model_manager.app.data_model import CivitAI_ModelId, CivitAI_ModelVersion, CivitAI_File, CivitAI_Image

@pytest.fixture(name="session")
def get_db_session():
    # engine = create_engine("sqlite:///:memory:")
    engine = create_engine(f"sqlite:///{Path(__file__).parent / 'db.sqlite3'}")
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def model_id_data():
    with open(Path(__file__).parent / 'model_id.json', mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())
        return CivitAI_ModelId(**data)

def test_sql_model_instantiation(model_id_data, session: Session):
    def convert_civitai_modelid_to_db_modelid(model_id: CivitAI_ModelId) -> Model_Id:
        def convert_civitai_modelversion_to_db_modelversion(model_version: CivitAI_ModelVersion) -> ModelVersion:
            def convert_civitai_modelversion_file_to_db_file(file: CivitAI_File) -> ModelVersionFile:
                record_file = ModelVersionFile(
                    id=file.id,
                    size_kb=file.sizeKB,
                    name=file.name,
                    type=file.type,
                    download_url=file.downloadUrl,
                    api_info_file=file.model_dump(),
                    model_version_id=model_version.id,
                    # model_version=record_model_version
                )
                return record_file
            def convert_civitai_modelversion_image_to_db_image(image: CivitAI_Image) -> ModelVersionImage:
                record_image = ModelVersionImage(
                    id=image.id,
                    url=image.url,
                    nsfw_level=image.nsfwLevel,
                    image_data=b'test',
                    api_info_image=image.model_dump(),
                    model_version_id=model_version.id,
                    # model_version=record_model_version
                )
                return record_image
            record_model_version = ModelVersion(
                id=model_version.id,
                name=model_version.name,
                base_model=model_version.baseModel,
                nsfw_level=model_version.nsfwLevel,
                model_id=model_id.id,
                api_info_model_version=model_version.model_dump(),
                images=[convert_civitai_modelversion_image_to_db_image(x) for x in model_version.images],
                files=[convert_civitai_modelversion_file_to_db_file(x) for x in model_version.files]
            )
            return record_model_version
        record_model_id = Model_Id(
            id=model_id.id,
            name=model_id.name,
            type=model_id.type,
            nsfw=model_id.nsfw,
            nsfw_level=model_id.nsfwLevel,
            api_info_model_id=model_id.model_dump(),
            model_versions=[convert_civitai_modelversion_to_db_modelversion(x) for x in model_id.modelVersions],
            tags=[Model_Tag(name=tag) for tag in model_id.tags]
        )
        return record_model_id
    model_id_ = convert_civitai_modelid_to_db_modelid(model_id_data)
    session.add(model_id_)
    session.commit()
    session.refresh(model_id_)
    
    assert model_id_data

def test_in_operator_in_sqlmodel(session: Session):
    from src.civitai_model_manager.app.api.v1.local_models import find_tags
    res = find_tags(tags=['test'], db_session=session)
    assert len(res.data) == 0

    res = find_tags(tags=['clothing'], db_session=session)
    assert len(res.data) == 1