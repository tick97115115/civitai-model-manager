from typing import Sequence
from sqlmodel import select, col
from pydantic import StrictInt, BaseModel
from ...data_model import CivitAI_ModelId, CivitAI_File, CivitAI_ModelVersion
from ...db.civitai_table import Model_Id, ModelVersion, Model_Tag, ModelIdTagLink
from ...dependencies import DbSessionDep, get_db_session, app
from ...data_model import API_Response_V1
import pydash as _

class Get_Tags_Response(API_Response_V1):
    data: Sequence[Model_Tag]

@app.get("/api/v1/local/tags", response_model=Get_Tags_Response)
def get_all_tags(db_session: DbSessionDep) -> Get_Tags_Response:
    statement = select(Model_Tag)
    result = db_session.exec(statement)
    return Get_Tags_Response(
        code=200,
        message="success",
        data=result.all()
    )

class Find_Tags_Response(API_Response_V1):
    data: Sequence[Model_Tag]

@app.post("/api/v1/local/tags/find", response_model=Find_Tags_Response)
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

@app.post("/api/v1/local/model_ids_by_tags", response_model=Find_Model_Ids_By_Tags_Response)
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
    statement = select(Model_Tag).where(col(Model_Tag.name).in_(tags))
    result = db_session.exec(statement)
    existed_tags = result.all()
    existed_tags_str = [tag.name for tag in existed_tags]
    tags_not_exists = _.difference(tags, existed_tags_str)
    
    tags_list: list[Model_Tag] = []

    if len(tags_not_exists) != 0:
        for tag_name in tags_not_exists:
            created_tag = Model_Tag(name=tag_name)
            db_session.add(created_tag)
            tags_list.append(created_tag)
        db_session.commit()
        for tag in tags_list:
            db_session.refresh(tag)
    tags_list.extend(existed_tags)
    return tags_list

class Get_Model_Id_Response(API_Response_V1):
    data: None | Model_Id

@app.get("/api/v1/local/model_id/{model_id}", response_model=Get_Model_Id_Response)
def find_one_model_id(model_id: StrictInt, db_session: DbSessionDep):
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
    
def create_one_model_id(model_id: CivitAI_ModelId, db_session: DbSessionDep) -> Model_Id:
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

def update_one_model_id(model_id: CivitAI_ModelId, model_id_record: Model_Id, db_session: DbSessionDep) -> Model_Id:
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
    tags_been_removed_records = find_or_create_tags(tags=tags_been_removed, db_session=db_session)
    for removed_tag_record in tags_been_removed_records:
        removed_tag_record.model_ids.remove(model_id_record)
    db_session.add(model_id_record)
    db_session.commit()
    db_session.refresh(model_id_record)
    return model_id_record

class CreateOrUpdateOneModelId(API_Response_V1):
    data: Model_Id

@app.post("/api/v1/local/model_id/create_or_update_one", response_model=CreateOrUpdateOneModelId)
def create_or_update_one_model_id(model_id: CivitAI_ModelId, db_session: DbSessionDep) -> CreateOrUpdateOneModelId:
    res = find_one_model_id(model_id=model_id.id, db_session=db_session)
    if (res.data == None):
        model_id_record = create_one_model_id(model_id=model_id, db_session=db_session)
        return CreateOrUpdateOneModelId(
            code=201,
            message="One new modelId created",
            data=model_id_record
        )
    else:
        model_id_record = update_one_model_id(model_id=model_id, model_id_record=res.data, db_session=db_session)
        return CreateOrUpdateOneModelId(
            code=200,
            message="One existed modelId updated",
            data=model_id_record
        )

