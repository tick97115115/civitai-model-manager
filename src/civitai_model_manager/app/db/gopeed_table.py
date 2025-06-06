from sqlmodel import SQLModel, Field, Relationship, JSON
from pydantic import StrictInt
from ..data_model import CivitAI_File, CivitAI_Image

class ModelVersionGopeedTask(SQLModel, table=True):
    version_id: StrictInt = Field(primary_key=True)
    model_id_api_info: dict = Field(sa_type=JSON)
    model_version_api_info: dict = Field(sa_type=JSON)
    image_tasks: list["ModelVersionImageGopeedTask"] = Relationship(back_populates="model_version_task", cascade_delete=True)
    file_tasks: list["ModelVersionFileGopeedTask"] = Relationship(back_populates="model_version_task", cascade_delete=True)

class ModelVersionFileGopeedTask(SQLModel, table=True):
    file_id: StrictInt = Field(primary_key=True)
    task_id: None | str = Field(default=None)
    finished: bool = Field(default=False)
    file_api_info: CivitAI_File = Field(sa_type=JSON)
    version_id: StrictInt = Field(foreign_key=f"{ModelVersionGopeedTask.__tablename__}.version_id", index=True, ondelete="CASCADE")
    model_version_task: ModelVersionGopeedTask = Relationship(back_populates="file_tasks")

class ModelVersionImageGopeedTask(SQLModel, table=True):
    image_id: StrictInt = Field(primary_key=True)
    finished: bool = Field(default=False)
    image_api_info: CivitAI_Image = Field(sa_type=JSON)
    version_id: StrictInt = Field(foreign_key=f"{ModelVersionGopeedTask.__tablename__}.version_id", index=True, ondelete="CASCADE")
    model_version_task: ModelVersionGopeedTask = Relationship(back_populates="image_tasks")
