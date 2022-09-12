import os
from typing import Optional, Union

import rsa
from dotenv import load_dotenv
from pydantic import BaseSettings

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()   # take environment variables from .env.


class JWTSettings(BaseSettings):
    """Setting for JWT Token"""

    JWT_SECRET_KEY: Union[str, bytes, rsa.PublicKey, rsa.PrivateKey]
    JWT_ALGORITHM: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class MongoUser(BaseSettings):
    """Mongo DB username and password"""

    MONGO_USER: Optional[str]
    MONGO_PASS: Optional[str]   # noqa: WPS115


class MongoSettingsProm(MongoUser):
    """Mongo DB host and port for production"""

    MONGO_HOST: Optional[str]
    MONGO_PORT: Optional[str]


class MongoSettingsDev(MongoUser):
    """Mongo DB host and port for development"""

    MONGO_HOST: Optional[str] = os.getenv('MONGO_HOST_DEBUG')  # noqa: WPS115
    MONGO_PORT: Optional[str] = os.getenv('MONGO_PORT_DEBUG')  # noqa: WPS115


class FastAPISettings(BaseSettings):
    FAST_API_HOST: Optional[str]
    FAST_API_PORT: Optional[str]


class SentrySettings(BaseSettings):
    sentry_dsn: Optional[str]
    traces_sample_rate: Optional[str]


class Settings(BaseSettings):

    PROJECT_NAME: Optional[str]
    TOPIC: Optional[str]

    jwt_settings: JWTSettings = JWTSettings()
    fast_api_settings: FastAPISettings = FastAPISettings()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


class PromSettings(Settings):
    mongo_settings: MongoSettingsProm = MongoSettingsProm()
    sentry: bool = True
    sentry_ssettings: SentrySettings = SentrySettings()


class DevSettings(Settings):
    mongo_settings: MongoSettingsDev = MongoSettingsDev()
    sentry: bool = False


def get_settings() -> Union[PromSettings, DevSettings]:
    environment = os.getenv('ENVIRONMENT')
    if environment == 'prom':
        return PromSettings()
    return DevSettings()


settings = get_settings()
