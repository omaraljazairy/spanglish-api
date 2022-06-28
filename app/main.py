import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.database import engine
from datamodels import models
from routers import (language, category, verb, word, translation, quiz, quizquestion,
                     quizresult)
from exceptions.model_exceptions import (NotFoundException, AlreadyExistsException,
                                         WordNotVerbException)
import logging.config
from app.log import LOGGING


logging.config.dictConfig(LOGGING)
models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('main')
logger.debug('main initialized')

app = FastAPI()
app.include_router(router=language.router)
app.include_router(router=category.router)
app.include_router(router=word.router)
app.include_router(router=verb.router)
app.include_router(router=translation.router)
app.include_router(router=quiz.router)
app.include_router(router=quizquestion.router)
app.include_router(router=quizresult.router)

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

@app.exception_handler(WordNotVerbException)
def not_verb_category_exception_handler(request: Request, exc: WordNotVerbException):
        return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.get("/")
async def main():
    return {
        "foo": "bar",
    }

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
