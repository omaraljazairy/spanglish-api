import logging
import os
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.main import app
from datamodels.models import (Category, Language, Quiz, QuizQuestion,
                               QuizResult, Translation, User, Verb, Word)
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
def created_user(db):
    """ create users to be used in the test"""

    session = db

    user_1 = User(
        id=1,
        username='test_user1',
        password='testpassword1',
        email='test1@test.com',
        fullname='test_test1'
    )
    session.add(user_1)
    session.commit()

    user_2 = User(
        id=2,
        username='test_user2',
        password='testpassword2',
        email='test2@test.com',
        fullname='test_test2'
    )
    session.add(user_2)
    session.commit()

    user_3 = User(
        id=3,
        username='test_user3',
        password='testpassword3',
        email='test3@test.com',
        fullname='test_test3'
    )
    session.add(user_3)
    session.commit()
    return (user_1, user_2, user_3)


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

    adjective = Category(id=4, name='Adjective')
    session.add(adjective)
    session.commit()

    feeling = Category(id=5, name='Feeling')
    session.add(feeling)
    session.commit()

    return (verb, day, place, adjective, feeling)


@pytest.fixture(scope="session")
def created_word(db):

    session = db

    hablar = Word(
        id=1,
        category_id=1,
        text='Hablar',
        translations=[
            Translation(language_id=1, translation='to speak'),
            Translation(language_id=1, translation='to talk')
        ]
    )
    session.add(hablar)

    jueves = Word(
        id=2,
        category_id=2,
        text='Jueves',
        translations=[
            Translation(language_id=1, translation='Thursday')
        ]
    )
    session.add(jueves)

    lunes = Word(
        id=3,
        category_id=2,
        text='Lunes',
        translations=[
            Translation(language_id=1, translation='Monday')
        ]
    )
    session.add(lunes)

    comer = Word(
        id=4,
        category_id=1,
        text='Comer',
        translations=[
            Translation(language_id=1, translation='Eat')
        ]
    )
    session.add(comer)

    ir = Word(
        id=5,
        category_id=1,
        text='Ir',
        translations=[
            Translation(language_id=1, translation='Go')
        ]
    )
    session.add(ir)

    bella = Word(
        id=6,
        category_id=4,
        text='Bonita',
        translations=[
            Translation(language_id=1, translation='Beautiful')
        ]
    )
    session.add(bella)
    session.commit()

    return (hablar, jueves, lunes, comer, ir, bella)


@pytest.fixture(scope="session")
def created_translation(db):

    session = db

    hablar = Translation(
        id=1,
        language_id=1,
        translation='to talk')
    session.add(hablar)
    session.commit()

    jueves = Translation(
        id=2,
        language_id=1,
        translation='Thursday')
    session.add(jueves)
    session.commit()

    lunes = Translation(
        id=3,
        language_id=1,
        translation='Monday')
    session.add(lunes)
    session.commit()

    comer = Translation(
        id=4,
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


@pytest.fixture(scope="session")
def created_quiz(db):

    session = db

    verbs = Quiz(id=1, title='Verbs', active=1)
    session.add(verbs)
    session.commit()

    days = Quiz(id=2, title='Days', active=1)
    session.add(days)
    session.commit()

    places = Quiz(id=3, title='Places', active=1)
    session.add(places)
    session.commit()

    adjectives = Quiz(id=4, title='Adjectives', active=0)
    session.add(adjectives)
    session.commit()

    test_1 = Quiz(id=5, title='Test_1', active=1)
    session.add(test_1)
    session.commit()

    test_2 = Quiz(id=6, title='Test_2', active=1)
    session.add(test_2)
    session.commit()

    return (verbs, days, places, adjectives, test_1, test_2)


@pytest.fixture(scope="session")
def created_quizquestion(db):

    session = db

    question_1 = QuizQuestion(
        id=1,
        quiz_id=1,
        word_id=1,
        question='what is the meaning of'
    )
    session.add(question_1)
    session.commit()

    question_2 = QuizQuestion(
        id=2,
        quiz_id=2,
        word_id=2,
        question='what is the meaning of'
    )
    session.add(question_2)
    session.commit()

    question_3 = QuizQuestion(
        id=3,
        quiz_id=3,
        word_id=3,
        question='what does this word mean'
    )
    session.add(question_3)
    session.commit()

    question_4 = QuizQuestion(
        id=4,
        quiz_id=4,
        word_id=1,
        question='what does this word mean'
    )
    session.add(question_4)
    session.commit()

    question_5 = QuizQuestion(
        id=5,
        quiz_id=5,
        word_id=5,
        question='what does this word mean'
    )
    session.add(question_5)
    session.commit()

    question_6 = QuizQuestion(
        id=6,
        quiz_id=2,
        word_id=4,
        question='what does this word mean'
    )
    session.add(question_6)
    session.commit()

    return (
        question_1,
        question_2,
        question_3,
        question_4,
        question_5,
        question_6
    )


@pytest.fixture(scope="session")
def created_quizresult(db):

    session = db

    result_1 = QuizResult(
        id=1,
        quizquestion_id=1,
        attempts=1,
        user_id=1,
        created=datetime.today() - timedelta(days=2)
    )
    session.add(result_1)
    session.commit()

    result_2 = QuizResult(
        id=2,
        quizquestion_id=2,
        attempts=3,
        user_id=1
    )
    session.add(result_2)
    session.commit()

    result_3 = QuizResult(
        id=3,
        quizquestion_id=3,
        attempts=2,
        user_id=1,
        created=datetime.today() - timedelta(days=1)
    )
    session.add(result_3)
    session.commit()

    result_4 = QuizResult(
        id=4,
        quizquestion_id=1,
        attempts=4,
        user_id=2,
        created=datetime.today() - timedelta(days=3)
    )
    session.add(result_4)
    session.commit()

    result_5 = QuizResult(
        id=5,
        quizquestion_id=2,
        attempts=1,
        user_id=2,
        created=datetime.today() - timedelta(days=2)
    )
    session.add(result_5)
    session.commit()

    result_6 = QuizResult(
        id=6,
        quizquestion_id=1,
        attempts=3,
        user_id=3
    )
    session.add(result_6)
    session.commit()

    return (
        result_1,
        result_2,
        result_3,
        result_4,
        result_5,
        result_6
    )
