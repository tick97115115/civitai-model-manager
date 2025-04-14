from enum import StrEnum
from pydantic import BaseModel, ConfigDict, StrictInt, HttpUrl
from datetime import datetime

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
    id: StrictInt
    url: HttpUrl
    nsfwLevel: StrictInt
    width: StrictInt
    height: StrictInt
    hash: str
    type: str

    model_config = ConfigDict(extra='allow')

class CivitAI_File_Metadata(BaseModel):
    format: str

    model_config = ConfigDict(extra='allow')

class CivitAI_File(BaseModel):
    id: StrictInt
    sizeKB: float
    name: str
    type: str
    scannedAt: None | datetime
    metadata: CivitAI_File_Metadata
    downloadUrl: HttpUrl

    model_config = ConfigDict(extra='allow')

class CivitAI_ModelVersion_Availability(StrEnum):
    EarlyAccess = 'EarlyAccess'
    Public = 'Public'

class CivitAI_ModelVersion(BaseModel):
    id: StrictInt
    index: StrictInt
    name: str
    baseModel: str
    baseModelType: None | str
    publishedAt: None | datetime # "2024-01-30T00:24:15.582Z",
    availability: CivitAI_ModelVersion_Availability
    nsfwLevel: StrictInt
    description: None | str # HTML string
    trainedWords: list[str]
    stats: dict
    files: list[CivitAI_File]
    images: list[CivitAI_Image]
    downloadUrl: HttpUrl

    model_config = ConfigDict(extra='allow')

class CivitAI_ModelId(BaseModel):
    id: StrictInt
    name: str
    description: None | str
    type: CivitAI_Model_Type
    poi: bool
    nsfw: bool
    nsfwLevel: StrictInt
    # cosmetic: None
    stats: dict
    tags: list[str]
    modelVersions: list[CivitAI_ModelVersion]

    model_config = ConfigDict(extra='allow')

class API_Response_V1(BaseModel):
    code: int
    message: str
