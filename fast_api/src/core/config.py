import os
from typing import Optional, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, BaseModel

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()   # take environment variables from .env.


class JWTSettings(BaseModel):
    """Setting for JWT Token"""

    JWT_SECRET_KEY: Optional[str] = os.getenv('JWT_SECRET_KEY')  # noqa: WPS115
    JWT_ALGORITHM: Optional[str] = os.getenv('JWT_ALGORITHM')  # noqa: WPS115


class MongoUser(BaseModel):
    """Mongo DB username and password"""

    MONGO_USER: Optional[str] = os.getenv('MONGO_USER')  # noqa: WPS115
    MONGO_PASS: Optional[str] = os.getenv('MONGO_PASS')  # noqa: WPS115


class MongoSettingsProm(MongoUser):
    """Mongo DB host and port for production"""

    MONGO_HOST: Optional[str] = os.getenv('MONGO_HOST')  # noqa: WPS115
    MONGO_PORT: Optional[str] = os.getenv('MONGO_PORT')  # noqa: WPS115


class MongoSettingsDev(MongoUser):
    """Mongo DB host and port for development"""

    MONGO_HOST: Optional[str] = os.getenv('MONGO_HOST_DEBUG')  # noqa: WPS115
    MONGO_PORT: Optional[str] = os.getenv('MONGO_PORT_DEBUG')  # noqa: WPS115


class FastAPISettings(BaseModel):
    FAST_API_HOST: Optional[str] = os.getenv('FAST_API_HOST')  # noqa: WPS115
    FAST_API_PORT: Optional[str] = os.getenv('FAST_API_PORT')  # noqa: WPS115


class Settings(BaseSettings):

    PROJECT_NAME: Optional[str] = os.getenv('PROJECT_NAME')  # noqa: WPS115

    TOPIC: Optional[str] = os.getenv('TOPIC')  # noqa: WPS115

    jwt_settings: JWTSettings = JWTSettings()

    fast_api_settings: FastAPISettings = FastAPISettings()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


class PromSettings(Settings):
    mongo_settings: MongoSettingsProm = MongoSettingsProm()


class DevSettings(Settings):
    mongo_settings: MongoSettingsDev = MongoSettingsDev()


def get_settings() -> Union[PromSettings, DevSettings]:
    environment = os.getenv('ENVIRONMENT')
    if environment == 'prom':
        return PromSettings()
    return DevSettings()


settings = get_settings()
