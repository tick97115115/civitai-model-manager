from enum import StrEnum
from pydantic import BaseModel, ConfigDict

class CivitAI_Model_Type(StrEnum):
    Checkpoint = 'Checkpoint'
    TextualInversion = 'TextualInversion'
    Hypernetwork = 'Hypernetwork'
    AestheticGradient = 'AestheticGradient'
    LORA = 'LORA'
    LoCon = 'LoCon'
    DoRA = 'DoRA'
    Controlnet = 'Controlnet'
    Upscaler = 'Upscaler'
    MotionModule = 'MotionModule'
    VAE = 'VAE'
    Poses = 'Poses'
    Wildcards = 'Wildcards'
    Workflows = 'Workflows'
    Detection = 'Detection'
    Other = 'Other'

class CivitAI_Image(BaseModel):
    id: int
    url: str
    nsfwLevel: int
    width: int
    height: int
    hash: str
    type: str

    model_config = ConfigDict(extra='allow')

    def get_image_filename(self) -> str:
        return self.url.rsplit('/', 1)[-1]

    def get_image_suffix(self) -> str:
        return self.get_image_filename().rsplit('.', 1)[-1]

class CivitAI_File_Metadata(BaseModel):
    format: str

    model_config = ConfigDict(extra='allow')

class CivitAI_File(BaseModel):
    id: int
    sizeKB: float
    name: str
    type: str
    scannedAt: None | str # ISO8061
    metadata: CivitAI_File_Metadata
    downloadUrl: str

    model_config = ConfigDict(extra='allow')

    def get_file_name(self) -> str:
        return self.name.rsplit('.', 1)[0]

class CivitAI_ModelVersion_Availability(StrEnum):
    EarlyAccess = 'EarlyAccess'
    Public = 'Public'

class CivitAI_ModelVersion(BaseModel):
    id: int
    index: int
    name: str
    baseModel: str
    baseModelType: None | str
    publishedAt: None | str # "2024-01-30T00:24:15.582Z", ISO8061
    availability: CivitAI_ModelVersion_Availability
    nsfwLevel: int
    description: None | str # HTML string
    trainedWords: list[str]
    stats: dict
    files: list[CivitAI_File]
    images: list[CivitAI_Image]
    downloadUrl: str

    model_config = ConfigDict(extra='allow')

class CivitAI_ModelId(BaseModel):
    id: int
    name: str
    description: None | str
    type: CivitAI_Model_Type
    poi: bool
    nsfw: bool
    nsfwLevel: int
    # cosmetic: None
    stats: dict
    tags: list[str]
    modelVersions: list[CivitAI_ModelVersion]

    model_config = ConfigDict(extra='allow')

class API_Response_V1(BaseModel):
    code: int
    message: str
