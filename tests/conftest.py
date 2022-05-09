import logging
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.main import app
from datamodels.models import Language
from services.database import Base, get_db

logger = logging.getLogger('fixtures')

# DB
DBNAME = "test"
DB_HOST = os.getenv("DB_HOST", False)
MYSQL_URL = f"mysql://{DBNAME}:@{DB_HOST}/{DBNAME}"
# TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_test_app.db"


@pytest.fixture(scope="session")
def db_engine():
    """create the database and return an instance of the engine."""

    engine = create_engine(MYSQL_URL, connect_args={})
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="session")
def db(db_engine):
    """setup the database connection and use the db_engine to use the test
    database. return a session to be available for all tests.
    """

    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)

    yield db

    db.rollback()
    connection.close()


# override the get_db to use the test db during the test session
app.dependency_overrides[get_db] = lambda: db


@pytest.fixture(scope="session")
def client(db):
    """create the test client using the test database to be available for
    all tests.
    """
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


# DB fixtures ###
@pytest.fixture(scope="session")
def create_language(db):

    session = db

    en_lan = Language(
        id=1,
        name='English',
        code='EN'
    )
    session.add(en_lan)
    session.commit()

    de_lan = Language(
        id=2,
        name='German',
        code='AR'
    )
    session.add(de_lan)
    session.commit()

    es_lan = Language(
        id=3,
        name='Spanish',
        code='ES'
    )
    session.add(es_lan)
    session.commit()
