from typing import Sequence
from sqlmodel import select, col
from pydantic import StrictInt
from ...data_model import CivitAI_ModelId
from ...db.civitai_table import Model_Id, ModelVersion, Model_Tag, ModelIdTagLink
from ...dependencies import DbSessionDep, get_db_session, app
from ...data_model import API_Response_V1
import pydash as _

class Get_Model_Id_Response(API_Response_V1):
    data: None | Model_Id

@app.get("/api/v1/models/{model_id}", response_model=Get_Model_Id_Response)
def get_model_id(model_id: StrictInt, db_session: DbSessionDep):
    statement = select(Model_Id).where(Model_Id.id == model_id)
    result = db_session.exec(statement)

    data = result.first()

    if data != None:
        return Get_Model_Id_Response(
            code=200,
            message="success",
            data=data
        )
    else:
        return Get_Model_Id_Response(
            code=404,
            message="Not Found",
            data=data
        )
    
class Get_Tags_Response(API_Response_V1):
    data: Sequence[Model_Tag]

@app.get("/api/v1/tags", response_model=Get_Tags_Response)
def get_tags(db_session: DbSessionDep) -> Get_Tags_Response:
    statement = select(Model_Tag)
    result = db_session.exec(statement)
    return Get_Tags_Response(
        code=200,
        message="success",
        data=result.all()
    )

class Find_Tags_Response(API_Response_V1):
    data: Sequence[Model_Tag]

def find_tags(tags: list[str], db_session: DbSessionDep) -> Find_Tags_Response:
    statement = select(Model_Tag).where(col(Model_Tag.name).in_(tags))
    result = db_session.exec(statement)
    return Find_Tags_Response(
        code=200,
        message="success",
        data=result.all()
    )

class Find_Model_Ids_By_Tags_Response(API_Response_V1):
    data: Sequence[Model_Id]

@app.post("/api/v1/tags", response_model=Find_Model_Ids_By_Tags_Response)
def find_model_ids_by_tags(tags: list[str], db_session: DbSessionDep) -> Find_Model_Ids_By_Tags_Response:
    statement = select(Model_Id).join(ModelIdTagLink).join(Model_Tag).where(col(Model_Tag.name).in_(tags)).distinct()
    result = db_session.exec(statement)
    return Find_Model_Ids_By_Tags_Response(
        code=200,
        message="success",
        data=result.all()
    )

def find_or_create_tag(tag_name: str, db_session: DbSessionDep) -> Model_Tag:
    statement = select(Model_Tag).where(Model_Tag.name == tag_name)
    result = db_session.exec(statement)
    tag = result.first()
    if tag == None:
        tag = Model_Tag(name=tag_name)
        db_session.add(tag)
        db_session.commit()
        db_session.refresh(tag)
        return tag
    else:
        return tag

def find_or_create_tags(tags: list[str], db_session: DbSessionDep) -> list[Model_Tag]:
    tag_list: list[Model_Tag] = []
    for tag_name in tags:
        tag_list.append(find_or_create_tag(tag_name=tag_name, db_session=db_session))
    return tag_list

def create_model_id(model_id: CivitAI_ModelId, db_session: DbSessionDep) -> Model_Id:
    tags = find_or_create_tags(model_id.tags, db_session=db_session)
    model_id_record = Model_Id(
        id=model_id.id,
        name=model_id.name,
        type=model_id.type,
        nsfw=model_id.nsfw,
        nsfw_level=model_id.nsfwLevel,
        api_info_model_id=model_id,
        model_versions=[],
        tags=tags
    )
    db_session.add(model_id_record)
    db_session.commit()
    db_session.refresh(model_id_record)
    return model_id_record

def update_model_id(model_id: CivitAI_ModelId, model_id_record: Model_Id, db_session: DbSessionDep) -> Model_Id:
    model_id_record.name = model_id.name
    model_id_record.type = model_id.type
    model_id_record.nsfw = model_id.nsfw
    model_id_record.nsfw_level = model_id.nsfwLevel
    model_id_record.api_info_model_id = model_id.model_dump()
    db_tags = [db_tag.name for db_tag in model_id_record.tags]
    tags_not_in_model_id = _.difference(model_id.tags, db_tags)
    for lacked_tag in tags_not_in_model_id:
        new_tag = find_or_create_tag(tag_name=lacked_tag, db_session=db_session)
        model_id_record.tags.append(new_tag)
    tags_been_removed = _.difference(db_tags, model_id.tags)
    for removed_tag in tags_been_removed:
        _tag = find_or_create_tag(tag_name=removed_tag, db_session=db_session)
        _tag.model_ids.remove(model_id_record)
    db_session.add(model_id_record)
    db_session.commit()
    db_session.refresh(model_id_record)
    return model_id_record

def update_or_create_model_id(model_id: CivitAI_ModelId, db_session: DbSessionDep) -> Model_Id:
    res = get_model_id(model_id=model_id.id, db_session=db_session)
    if (res.data == None):
        return create_model_id(model_id=model_id, db_session=db_session)
    else:
        model_id_record = update_model_id(model_id=model_id, model_id_record=res.data, db_session=db_session)
    return model_id_record
    
