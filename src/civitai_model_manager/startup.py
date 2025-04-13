from fastapi import FastAPI
from pydantic_settings import BaseSettings
from pydantic import Field
import httpx
from os.path import join, dirname, exists
from urllib.parse import urljoin
import json
from gospeed_api.index import GospeedAPI

app = FastAPI()

settings_file = join(dirname(__file__), 'settings.json')
sqlite_file = join(dirname(__file__), 'db.sqlite3')

class Settings(BaseSettings):
    db_uri: str = Field(default='sqlite:///' + sqlite_file)
    resources_folder: str = ''
    proxy: str = ''
    api_key: str = ''
    gopeed_url: str = ''

# router = APIRouter()

# https://fastapi.tiangolo.com/tutorial/handling-errors/?h=exce#install-custom-exception-handlers

class LoadSettingsError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg

# @app.exception_handler(LoadSettingsError)
# async def load_settings_exception_handler(request: Request, exc: LoadSettingsError):
#     return JSONResponse(
#         status_code=500,
#         content={"message": exc.msg},
#     )

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

class LoraFolderNotFound(Exception):
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

def check_settings(settings: Settings):
    # check if lora_folder exists
    if not exists(settings.resources_folder):
        raise LoraFolderNotFound(msg="lora folder doesn't exists")

    # check if gopeed_url exists
    if not settings.gopeed_url:
        raise GopeedServiceNotFound(msg="gopeed service url not found")
    
    # check if gopeed service is working
    response = httpx.get(urljoin(settings.gopeed_url, '/api/v1/info'))
    if response.status_code != 200:
        raise GopeedServiceNotWorking(msg="gopeed service not working")
    
    # check database
    # if not exists(settings.db_uri):
    #     raise DatabaseNotFound(msg="database doesn't exists")

# @router.get("/settings", response_model=Settings)
def load_settings() -> Settings:
    # if file content broken makes it un deserializable
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            # if settings option value (like lora_folder) can't be found
            settings = Settings(**data)
            check_settings(settings)
            return settings
    except Exception as e:
        raise e

# @router.post("/settings")
def save_settings(settings: Settings):
    with open(settings_file, 'w', encoding="utf-8") as f:
        f.write(settings.model_dump_json(indent=2))

# @router.get("/settings/reset")
def reset_settings():
    settings = Settings()
    save_settings(settings)

def init() -> Settings:
    initial_check_pass: bool = False
    settings: Settings

    while not initial_check_pass:
        # check if settings file exists
        if not exists(settings_file):
            print("settings file not found, creating new one.")
            reset_settings()
            continue

        # check if settings are correct
        try:
            settings = load_settings()
            check_settings(settings)
        except LoadSettingsError:
            print("Load settings.json failed!!!")
            input(f"Please edit \"{settings_file}\", then Press enter to continue...")
            continue
        except LoraFolderNotFound:
            print("Lora folder not found")
            input("please check \"lora_folder\" value in \".settings.json\" then Press enter to continue...")
            continue
        except GopeedServiceNotWorking:
            print("Gopeed service not working")
            input("please check \"gopeed_url\" value in \".settings.json\" then Press enter to continue...")
            continue
        # except DatabaseNotFound:
        #     print("Database not found, is this your first time running the app?")
        #     answer = input("(Y/N): ")
        #     if answer.lower() == 'y':
        #         print("Creating new database...")
        #         from sqlmodel import create_engine, SQLModel, Session
        #         SQLModel.metadata.create_all(engine)
        #     else:
        #         print("Please check \"db_uri\" value in \".settings.json\"")
        #         input("Press enter to continue...")
        #     continue

        initial_check_pass = True
    
    return settings

settings = init()

gospeed_api = GospeedAPI(gopeed_host=settings.gopeed_url)

async_httpx_client = httpx.AsyncClient(proxy=settings.proxy)
httpx_client = httpx.Client(proxy=settings.proxy)