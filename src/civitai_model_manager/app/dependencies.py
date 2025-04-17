from fastapi import Depends, FastAPI
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import Engine
from contextlib import contextmanager
from typing import Annotated

from pathlib import Path

from anyio import open_file
from pydantic_settings import BaseSettings
from pydantic import Field
import httpx
from os.path import join, dirname, exists
from urllib.parse import urljoin
import json
from gospeed_api.index import GospeedAPI
from .data_model import CivitAI_ModelId, CivitAI_ModelVersion

app = FastAPI()

# router = APIRouter()

# https://fastapi.tiangolo.com/tutorial/handling-errors/?h=exce#install-custom-exception-handlers

class DatabaseNotFound(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

# @app.exception_handler(DatabaseNotFound)
# async def database_not_found_exception_handler(request: Request, exc: DatabaseNotFound):
#     return JSONResponse(
#         status_code=500,
#         content={"message": exc.msg},
#     )

class ModelsFolderNotFound(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

# @app.exception_handler(LoraFolderNotFound)
# async def lora_folder_not_found_exception_handler(request: Request, exc: LoraFolderNotFound):
#     return JSONResponse(
#         status_code=500,
#         content={"message": exc.msg},
#     )

class GopeedServiceNotFound(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
    
# @app.exception_handler(GopeedServiceNotFound)
# async def gopeed_service_not_found_exception_handler(request: Request, exc: GopeedServiceNotFound):
#     return JSONResponse(
#         status_code=500,
#         content={"message": exc.msg},
#     )

class GopeedServiceNotWorking(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

# @app.exception_handler(GopeedServiceNotWorking)
# async def gopeed_service_not_working_exception_handler(request: Request, exc: GopeedServiceNotWorking):
#     return JSONResponse(
#         status_code=500,
#         content={"message": exc.msg},
#     )

# @app.exception_handler(LoadSettingsError)
# async def load_settings_exception_handler(request: Request, exc: LoadSettingsError):
#     return JSONResponse(
#         status_code=500,
#         content={"message": exc.msg},
#     )

class SettingsJsonFileInvalideException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

settings_file = Path(__file__).parent / 'settings.json'
sqlite_file = join(dirname(__file__), 'db.sqlite3')

class SettingsJsonModel(BaseSettings):
    db_uri: str = Field(default='sqlite:///' + sqlite_file)
    resources_folder: str = ''
    proxy: str = ''
    api_key: str = ''
    gopeed_url: str = ''

class Settings:
    def __init__(self, settings_file_path: Path = settings_file, json_data: None | SettingsJsonModel = None):
        self.settings_file_path = settings_file_path
        self.json_data: None | SettingsJsonModel = json_data

    async def read_from_file(self):
        if not self.settings_file_path.exists():
            raise FileNotFoundError()
        async with await open_file(self.settings_file_path, 'r', encoding='utf-8') as f:
            try:
                contents = await json.loads(await f.read())
            except:
                raise SettingsJsonFileInvalideException(f"settings.json file content is invalied, see: {self.settings_file_path}")
            try:
                self.json_data = SettingsJsonModel(**contents)
            except Exception as e:
                raise SettingsJsonFileInvalideException(f"settings.json file content is invalied, pydantic error info:\n{str(e)}")
            return self.json_data

    async def get_json_settings_data(self):
        if self.json_data == None:
            await self.read_from_file()
        return self.json_data
    
    async def create_template_settings_json(self):
        async with await open_file(self.settings_file_path, 'w', encoding='utf-8') as f:
            await f.write(SettingsJsonModel().model_dump_json(indent=2))

    async def save_to_file(self):
        async with await open_file(self.settings_file_path, 'w', encoding='utf-8') as f:
            contents = await f.write(self.json_data.model_dump_json(indent=2))
    
    async def check_gopeed_service(self):
        settings_data = await self.get_json_settings_data()
        async with httpx.AsyncClient() as async_httpx_client:
            response = await async_httpx_client.get(urljoin(settings_data.gopeed_url, '/api/v1/info'))
            if response.status_code != 200:
                raise GopeedServiceNotWorking(msg="gopeed service not working")
        
    async def check_settings(self):
        settings_data = await self.get_json_settings_data()
        # check if lora_folder exists
        if not exists(settings_data.resources_folder):
            raise ModelsFolderNotFound(msg="lora folder doesn't exists")

        # check if gopeed_url exists
        if not settings_data.gopeed_url:
            raise GopeedServiceNotFound(msg="gopeed service url not found")
        
        # check if gopeed service is working
        async with httpx.AsyncClient() as async_httpx_client:
            response = await async_httpx_client.get(urljoin(settings_data.gopeed_url, '/api/v1/info'))
            if response.status_code != 200:
                raise GopeedServiceNotWorking(msg="gopeed service not working")

_settings = Settings()

def get_settings_dep():
    return _settings

SettingsDep = Annotated[Settings, Depends(get_settings_dep)]

async_httpx_client: None | httpx.AsyncClient = None

async def get_async_httpx_client(settings: SettingsDep):
    global async_httpx_client
    if async_httpx_client == None:
        settings_data = await settings.get_json_settings_data()
        async_httpx_client == httpx.AsyncClient(proxy=settings_data.proxy)
        return async_httpx_client
    else:
        return async_httpx_client

AsyncHttpxClientDep = Annotated[httpx.AsyncClient, Depends(get_async_httpx_client)]

httpx_client: None | httpx.Client = None

async def get_httpx_client(settings: SettingsDep):
    global httpx_client
    if httpx_client == None:
        settings_data = await settings.get_json_settings_data()
        async_httpx_client == httpx.Client(proxy=settings_data.proxy)
        return httpx_client
    else:
        return httpx_client
    
HttpxClientDep = Annotated[httpx.Client, Depends(get_httpx_client)]

gopeed_client: None | GospeedAPI = None

async def get_gopeed_client(settings: SettingsDep):
    global gopeed_client
    if gopeed_client == None:
        settings_data = await settings.get_json_settings_data()
        gopeed_client = GospeedAPI(gopeed_host=settings_data.gopeed_url)
        return gopeed_client
    else:
        return gopeed_client

GopeedClientDep = Annotated[GospeedAPI, Depends()]

engine: None | Engine = None

async def get_db_engine(settings: SettingsDep):
    global engine
    if engine == None:
        settings_data = await settings.get_json_settings_data()
        engine = create_engine(settings_data.db_uri)
        SQLModel.metadata.create_all(engine)
        return engine
    else:
        return engine

DbEngineDep = Annotated[Engine, Depends(get_db_engine)]

@contextmanager
async def get_db_session(engine: DbEngineDep):
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

DbSessionDep = Annotated[Session, Depends(get_db_session)]
