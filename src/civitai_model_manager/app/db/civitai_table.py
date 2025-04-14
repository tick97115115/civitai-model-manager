from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, LargeBinary
from pydantic import StrictInt
from ..data_model import CivitAI_Model_Type

# def get_model_type_dir(model_type: CivitAI_Model_Type):
#     return Path(settings.resources_folder) / model_type

class ModelIdTagLink(SQLModel, table=True):
    model_id: StrictInt | None = Field(default=None, foreign_key="model_id.id", primary_key=True)
    tag_id: StrictInt | None = Field(default=None, foreign_key="model_tag.id", primary_key=True)

class Model_Id(SQLModel, table=True):
    id: StrictInt = Field(primary_key=True)
    name: str = Field(index=True)
    type: CivitAI_Model_Type = Field(index=True)
    nsfw: bool
    nsfw_level: StrictInt
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
    id: StrictInt | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    model_ids: list[Model_Id] = Relationship(back_populates="tags", link_model=ModelIdTagLink)

class ModelVersion(SQLModel, table=True):
    id: StrictInt = Field(primary_key=True)
    name: str = Field(index=True)
    base_model: str = Field(index=True)
    base_model_type: None | str
    nsfw_level: StrictInt
    model_id: StrictInt = Field(foreign_key="model_id.id", ondelete="CASCADE")
    model: Model_Id = Relationship(back_populates="model_versions")
    api_info_model_version: dict = Field(sa_type=JSON)
    images: list["ModelVersionImage"] = Relationship(back_populates="model_version", cascade_delete=True)
    files: list["ModelVersionFile"] = Relationship(back_populates="model_version", cascade_delete=True)

    # def get_model_version_folder_path(self) -> Path:
    #     path = self.model.get_model_folder_path() / str(self.id)
    #     return path

class ModelVersionImage(SQLModel, table=True):
    id: StrictInt = Field(primary_key=True)
    url: str
    nsfw_level: StrictInt
    image_data: bytes = Field(sa_type=LargeBinary)
    api_info_image: dict = Field(sa_type=JSON)
    model_version_id: StrictInt = Field(foreign_key=f"{ModelVersion.__tablename__}.id", ondelete="CASCADE")
    model_version: ModelVersion = Relationship(back_populates="images")
    
    # def get_file_name(self) -> str:
    #     """
    #     截取URL路径的最后一段
        
    #     参数:
    #         url: 要处理的URL字符串，例如：
    #             "https://example.com/path/to/item.jpg"
                
    #     返回:
    #         路径的最后一段，例如 "item.jpg"
            
    #     示例:
    #         >>> get_last_url_segment("https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/.../width=450/34485305.jpeg")
    #         '34485305.jpeg'
    #     """
    #     # 解析URL获取路径部分
    #     # path = urlparse(str(self.url)).path
    #     path = self.url if self.url else ''

    #     # 标准化路径并分割
    #     segments = path.strip('/').split('/')
        
    #     # 返回最后一段（确保空URL安全）
    #     return segments[-1] if segments else ''

# extra_network_types = [CivitAI_Model_Type.LORA, CivitAI_Model_Type.DoRA, CivitAI_Model_Type.LoCon]

class ModelVersionFile(SQLModel, table=True):
    id: StrictInt = Field(primary_key=True)
    size_kb: float
    name: str
    type: str
    download_url: str
    api_info_file: dict = Field(sa_type=JSON)
    model_version_id: StrictInt = Field(foreign_key=f"{ModelVersion.__tablename__}.id", ondelete="CASCADE")
    model_version: ModelVersion = Relationship(back_populates="files")

    # def get_file_name(self) -> str:
    #     return f"{self.id}_{self.name}"

    # def get_file_path(self) -> Path:
    #     path = self.model_version.get_model_version_folder_path() / self.get_file_name()
    #     return path
    
    # def exists(self) -> bool:
    #     return self.get_file_path().exists()
