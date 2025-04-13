from sqlmodel import SQLModel, Field, Relationship, JSON
from pydantic import StrictInt
from pathlib import Path
from gospeed_api.models.create_a_task import CreateTask_DownloadOpt
from gospeed_api.models import Request_Extra_Opt, CreateTask_DownloadOpt_Extra
from .civitai_table import Model_Id, ModelIdTagLink, ModelVersion, ModelVersionFile, ModelVersionImage, get_model_type_dir
from ..data_model import CivitAI_ModelId, CivitAI_ModelVersion, CivitAI_File, CivitAI_Image

class ModelVersionGopeedTask(SQLModel, table=True):
    version_id: StrictInt = Field(primary_key=True)
    model_id_api_info: CivitAI_ModelId = Field(sa_type=JSON)
    model_version_api_info: ModelVersion = Field(sa_type=JSON)
    image_tasks: list["ModelVersionImageGopeedTask"] = Relationship(back_populates="model_version_task", cascade_delete=True)
    file_tasks: list["ModelVersionFileGopeedTask"] = Relationship(back_populates="model_version_task", cascade_delete=True)

    def get_model_version_path(self) -> Path:
        return get_model_type_dir(self.model_id_api_info.type) / str(self.model_id_api_info.id) / str(self.model_version_api_info.id)

class ModelVersionFileGopeedTask(SQLModel, table=True):
    file_id: StrictInt = Field(primary_key=True)
    task_id: None | str = Field(default=None)
    finished: bool = Field(default=False)
    file_api_info: CivitAI_File = Field(sa_type=JSON)
    version_id: StrictInt = Field(foreign_key=f"{ModelVersionGopeedTask.__tablename__}.version_id", index=True, ondelete="CASCADE")
    model_version_task: ModelVersionGopeedTask = Relationship(back_populates="file_tasks")

    def get_file_path(self) -> Path:
        return self.model_version_task.get_model_version_path() / f"{self.file_api_info.id}_{self.file_api_info.name}"

class ModelVersionImageGopeedTask(SQLModel, table=True):
    image_id: StrictInt = Field(primary_key=True)
    finished: bool = Field(default=False)
    image_api_info: CivitAI_Image = Field(sa_type=JSON)
    version_id: StrictInt = Field(foreign_key=f"{ModelVersionGopeedTask.__tablename__}.version_id", index=True, ondelete="CASCADE")
    model_version_task: ModelVersionGopeedTask = Relationship(back_populates="image_tasks")
