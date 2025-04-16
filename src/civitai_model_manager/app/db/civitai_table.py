from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, LargeBinary
from ..data_model import CivitAI_Model_Type

class ModelIdTagLink(SQLModel, table=True):
    model_id: int | None = Field(default=None, foreign_key="model_id.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="model_tag.id", primary_key=True)

class Model_Id(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    type: str = Field(index=True)
    nsfw: bool
    nsfw_level: int
    api_info_model_id: dict = Field(sa_type=JSON)
    model_versions: list["ModelVersion"] = Relationship(back_populates="model", cascade_delete=True)
    tags: list["Model_Tag"] = Relationship(back_populates="model_ids", link_model=ModelIdTagLink)

    # def get_model_folder_path(self) -> Path:
    #     path = get_model_type_dir(self.type) / str(self.id)
    #     return path
    
    # def save_api_info_json(self) -> None:
    #     json_path = self.get_model_folder_path() / "api_info.json"
    #     self.get_model_folder_path().mkdir(parents=True, exist_ok=True)
    #     with open(json_path, 'w', encoding='utf-8') as f:
    #         json.dump(self.api_info_model_id, f, indent=2)

class Model_Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    model_ids: list[Model_Id] = Relationship(back_populates="tags", link_model=ModelIdTagLink)

class ModelVersion(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    base_model: str = Field(index=True)
    downloaded: bool = False
    base_model_type: None | str
    nsfw_level: int
    model_id: int = Field(foreign_key="model_id.id", ondelete="CASCADE")
    model: Model_Id = Relationship(back_populates="model_versions")
    api_info_model_version: dict = Field(sa_type=JSON)
