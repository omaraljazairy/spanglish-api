from sqlalchemy.orm import Session
from datamodels.models import Quiz
from datamodels.schemas.quiz import QuizInsert, QuizUpdate
from exceptions.model_exceptions import AlreadyExistsException, NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_quizs(db: Session):
    """return all data from the quiz model."""

    return db.query(Quiz).all()


def create(db: Session, request: QuizInsert):
    """create a new Quiz object. check first if the records doesn't exist."""

    existing_quiz = db.query(Quiz).filter(
    Quiz.title == request.title
    ).first()
    
    if existing_quiz:
        logger.error(f"existing_quiz => {existing_quiz}")
        raise AlreadyExistsException(
            msg=f"Quiz {request.title} already exists"
        )

    db_quiz = Quiz(
        **request.dict()
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def update(db: Session, request: QuizUpdate, quiz_id: int):
    """
    update the quiz model. take the QuizUpdate schema and a 
    quiz_id as params. returns a quiz object.
    """
    db_quiz = db.query(Quiz).get(quiz_id)
    # throw an exception if not found
    if not db_quiz:
        raise NotFoundException(
            msg=f"quiz with id {quiz_id} is not found"
        )
    
    requested_quiz = request.dict(exclude_unset=True)
    for key, value in requested_quiz.items():
        setattr(db_quiz, key, value)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def delete(db: Session, quiz_id: int ) -> None:
    """delete the quiz object if found, else raise an exception."""

    db_quiz = db.query(Quiz).get(quiz_id)
    # throw an exception if not found
    if not db_quiz:
        raise NotFoundException(
            msg=f"quiz with id {quiz_id} doesn't exist"
        )
    db.delete(db_quiz)
    db.commit()
