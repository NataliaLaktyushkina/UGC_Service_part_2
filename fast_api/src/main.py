import motor.motor_asyncio
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse

from api.v1 import bookmarks
from api.v1 import likes
from core.config import settings
from db import mongo_db
from services.jwt_check import JWTBearer

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

PROTECTED = [Depends(JWTBearer())]


@app.on_event('startup')
async def startup():
    mongo_settings = settings.mongo_settings
    mongo_db.mongo_db = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.MONGO_HOST,
                                                               int(mongo_settings.MONGO_PORT),
                                                               username="rootuser",
                                                               password="rootpass")


# @app.on_event('shutdown')
# async def shutdown():
#     await eventbus_kafka.db_kafka.stop()


app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'], dependencies=PROTECTED)
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'], dependencies=PROTECTED)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8101,
    )
