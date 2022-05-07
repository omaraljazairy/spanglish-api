import logging
from fastapi import FastAPI
from services.database import engine
from datamodels import models
import logging.config
from app.log import LOGGING


logging.config.dictConfig(LOGGING)
models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('main')
app = FastAPI()
logger.debug('main initialized')

@app.get("/")
async def main():
    return {
        "foo": "bar",
    }
