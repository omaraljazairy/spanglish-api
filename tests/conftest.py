import logging
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.main import app
from datamodels.models import Category, Language, Translation, Verb, Word
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
def created_language(db):

    session = db

    en_lan = Language(id=1, name='English', code='EN')
    session.add(en_lan)
    session.commit()

    de_lan = Language(id=2, name='German', code='AR')
    session.add(de_lan)
    session.commit()

    es_lan = Language(id=3, name='Spanish', code='ES')
    session.add(es_lan)
    session.commit()

    return (en_lan, de_lan, es_lan)


@pytest.fixture(scope="session")
def created_category(db):

    session = db

    verb = Category(id=1, name='Verb')
    session.add(verb)
    session.commit()

    day = Category(id=2, name='Day')
    session.add(day)
    session.commit()

    place = Category(id=3, name='Place')
    session.add(place)
    session.commit()

    place = Category(id=4, name='Adjective')
    session.add(place)
    session.commit()
    return (verb, day, place)


@pytest.fixture(scope="session")
def created_word(db):

    session = db

    hablar = Word(id=1, category_id=1, text='Hablar')
    session.add(hablar)
    session.commit()

    jueves = Word(id=2, category_id=2, text='Jueves')
    session.add(jueves)
    session.commit()

    lunes = Word(id=3, category_id=2, text='Lunes')
    session.add(lunes)
    session.commit()

    comer = Word(id=4, category_id=1, text='Comer')
    session.add(comer)
    session.commit()

    ir = Word(id=5, category_id=1, text='Ir')
    session.add(ir)
    session.commit()

    bella = Word(id=6, category_id=4, text='beautiful')
    session.add(bella)
    session.commit()

    return (hablar, jueves, lunes, comer, ir, bella)


@pytest.fixture(scope="session")
def created_translation(db):

    session = db

    hablar = Translation(
        id=1,
        word_id=1,
        language_id=1,
        translation='to talk')
    session.add(hablar)
    session.commit()

    jueves = Translation(
        id=2,
        word_id=2,
        language_id=1,
        translation='Thursday')
    session.add(jueves)
    session.commit()

    lunes = Translation(
        id=3,
        word_id=3,
        language_id=1,
        translation='Monday')
    session.add(lunes)
    session.commit()

    comer = Translation(
        id=4,
        word_id=4,
        language_id=1,
        translation='to eat')
    session.add(comer)
    session.commit()

    return (hablar, jueves, lunes, comer)


@pytest.fixture(scope="session")
def created_verb(db):

    session = db

    hablar = Verb(
        id=1,
        word_id=1,
        yo='Hablo',
        tu='Hablas',
        el_ella_usted='Habla',
        nosotros='hablamos',
        vosotros='hablais',
        ellos_ellas_ustedes='hablan'
    )
    session.add(hablar)
    session.commit()

    comer = Verb(
        id=2,
        word_id=4,
        yo='Como',
        tu='comes',
        el_ella_usted='come',
        nosotros='comemos',
        vosotros='comeis',
        ellos_ellas_ustedes='comen'
    )
    session.add(comer)
    session.commit()

    return (hablar, comer)
