import logging
from typing import Any, Tuple
from typing import MutableMapping

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.responses import ORJSONResponse
from motor import motor_asyncio

from api.v1 import bookmarks
from api.v1 import critique
from api.v1 import likes
from core.config import settings
from db import mongo_db
from services.jwt_check import JWTBearer

sentry_sdk.init(
    dsn="https://bdac46e09f9444d1a209a8e570f92255@o1386750.ingest.sentry.io/6707192",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler отвечают за вывод и отправку сообщений. В модуль logging доступно несколько классов-обработчиков
# Например, SteamHandler для записи в поток stdin/stdout, DatagramHandler для UDP, FileHandler для syslog
# LogstashHandler не только отправляет данные по TCP/UDP, но и форматирует логи в json-формат.
stdout_handler = logging.StreamHandler()

logger.addHandler(stdout_handler)
PROTECTED = [Depends(JWTBearer)]  # noqa: WPS407


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg: Any,
                kwargs: MutableMapping[str, Any]) -> Tuple[Any, MutableMapping[str, Any]]:
        return self.extra['request_id'], kwargs


logger_a = CustomAdapter(logger, {"request_id": None})


@app.on_event('startup')
async def startup() -> None:
    """Start up settings - connect to Mongo DB"""
    mongo_settings = settings.mongo_settings
    mongo_db.mongo_db = motor_asyncio.AsyncIOMotorClient(
        mongo_settings.MONGO_HOST,
        int(mongo_settings.MONGO_PORT),  # type: ignore
        username=mongo_settings.MONGO_USER,
        password=mongo_settings.MONGO_PASS,
    )
    logger.info(msg='Successfull connect to DB')


@app.middleware("http")
async def before_request(request: Request, call_next):  # type: ignore
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        logger.warning(f'request_id {request_id}')
        raise RuntimeError('request id is required')
    return await call_next(request)


app.include_router(
    bookmarks.router, prefix='/api/v1/bookmarks',
    tags=['bookmarks'], dependencies=PROTECTED,
)

app.include_router(
    likes.router, prefix='/api/v1/likes',
    tags=['likes'], dependencies=PROTECTED,
)

app.include_router(
    critique.router, prefix='/api/v1/critique',
    tags=['critique'], dependencies=PROTECTED,
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8101,
    )
