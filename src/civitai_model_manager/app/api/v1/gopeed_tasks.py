
from typing import Sequence
from pathlib import Path
import httpx
from sqlmodel import select
from pydantic import StrictInt
from gospeed_api.models import Request_Extra_Opt, CreateTask_DownloadOpt
from .local_models import get_model_id, find_or_create_tags
import pydash as _
from ...db.civitai_table import ModelVersionImage, ModelVersion
from ...db.gopeed_table import ModelVersionGopeedTask, ModelVersionFileGopeedTask, ModelVersionImageGopeedTask
from ...data_model import API_Response_V1, CivitAI_ModelId
from ...dependencies import DbSessionDep, get_db_session, app, AsyncHttpxClientDep

class TaskConsumer:
    current_task: None | ModelVersionGopeedTask = None

    def find_a_task(self):
        with get_db_session() as session:
            statement = select(ModelVersionGopeedTask)
            result = session.exec(statement)

            self.current_task = result.first()
            if self.current_task != None:
                for image_task in self.current_task.image_tasks:
                    img = httpx.get(url=image_task.image_api_info.url)
                    get_model_id()

class API_Response_V1_GopeedTasks(API_Response_V1):
    data: Sequence[ModelVersionGopeedTask]

@app.get('/api/v1/gopeed_tasks', response_model=API_Response_V1_GopeedTasks)
def get_all_gopeed_tasks(db_session: DbSessionDep):
    statement = select(ModelVersionGopeedTask)
    result = db_session.exec(statement)
    return API_Response_V1_GopeedTasks(code=0, message="success", data=result.all())

@app.post('/api/v1/gopeed_tasks/{version_id}')
def add_task(model_id: CivitAI_ModelId, version_id: StrictInt, db_session: DbSessionDep):
    model_version = _.find(model_id.modelVersions, lambda x: x.id == version_id)
    if model_version == None:
        print(f"have no specific version_id {version_id} in modelid!!!")
        print(model_id.model_dump_json(indent=2))
    else:

        model_version_task = ModelVersionGopeedTask(
            version_id=version_id,
            model_id_api_info=model_id,
            model_version_api_info=model_version,
            image_tasks=[],
            file_tasks=[]
        ) 
        for file in model_version.files:
            file_task = ModelVersionFileGopeedTask(
                file_id=file.id,
                file_api_info=file,
                version_id=version_id,
                model_version_task=model_version_task
            )
            model_version_task.file_tasks.append(file_task)
        for image in model_version.images:
            image_task = ModelVersionImageGopeedTask(
                image_id=image.id,
                image_api_info=image,
                version_id=version_id,
                model_version_task=model_version_task
            )
            model_version_task.image_tasks.append(image_task)
        db_session.add(model_version_task)
        db_session.commit()

@app.get('/api/v1/gopeed_tasks/{version_id}/images/download')
async def download_image(version_id: StrictInt, db_session: DbSessionDep, async_httpx_client: AsyncHttpxClientDep):
    statement = select(ModelVersionGopeedTask).where(ModelVersionGopeedTask.version_id == version_id)
    result = db_session.exec(statement)
    model_version = db_session.exec(select(ModelVersion).where(ModelVersion.id == version_id)).first()

    data = result.first()
    if (data == None):
        print("not exists")
    else:
        for image_task in data.image_tasks:
            # image_task.
            res = await async_httpx_client.get(str(image_task.image_api_info.url))
            record = ModelVersionImage(
                id=image_task.image_id,
                url=image_task.image_api_info.url,
                nsfw_level=image_task.image_api_info.nsfwLevel,
                image_data=res.content,
                api_info_image=image_task.image_api_info,
                model_version_id=version_id,
                model_version=ModelVersion
            )
            db_session.add(record)
            db_session.commit()
            
