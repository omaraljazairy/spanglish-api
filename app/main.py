import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from services.database import engine
from datamodels import models
from routers import language
from exceptions.model_exceptions import NotFoundException, AlreadyExistsException
import logging.config
from app.log import LOGGING


logging.config.dictConfig(LOGGING)
models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('main')
logger.debug('main initialized')

app = FastAPI()
app.include_router(router=language.router)


# exception handlers
@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

@app.exception_handler(AlreadyExistsException)
def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
        return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

@app.get("/")
async def main():
    return {
        "foo": "bar",
    }
