from sqlalchemy.orm import Session
from datamodels.models import QuizQuestion
from datamodels.schemas.quizquestion import QuizQuestionInsert, QuizQuestionUpdate
from exceptions.model_exceptions import AlreadyExistsException, NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_quizquestions(db: Session):
    """return all data from the quizquestion model."""

    return db.query(QuizQuestion).all()


def create(db: Session, request: QuizQuestionInsert):
    """create a new QuizQuestion object. check first if the records doesn't exist."""

    existing_quizquestion = db.query(QuizQuestion).filter(
    QuizQuestion.quiz_id == request.quiz_id, QuizQuestion.word_id == request.word_id
    ).first()
    
    if existing_quizquestion:
        logger.error(f"existing_quizquestion => {existing_quizquestion}")
        raise AlreadyExistsException(
            msg=f"QuizQuestion with quiz_id {request.quiz_id} and word_id\
 {request.word_id} already exists"
        )

    db_quizquestion = QuizQuestion(
        **request.dict()
    )
    db.add(db_quizquestion)
    db.commit()
    db.refresh(db_quizquestion)
    return db_quizquestion


def update(db: Session, request: QuizQuestionUpdate, quizquestion_id: int):
    """
    update the quizquestion model. take the QuizQuestionUpdate schema and a 
    quizquestion_id as params. returns a quizquestion object.
    """
    db_quizquestion = db.query(QuizQuestion).get(quizquestion_id)
    # throw an exception if not found
    if not db_quizquestion:
        raise NotFoundException(
            msg=f"quizquestion with id {quizquestion_id} is not found"
        )
    
    requested_quizquestion = request.dict(exclude_unset=True)
    for key, value in requested_quizquestion.items():
        setattr(db_quizquestion, key, value)
    db.add(db_quizquestion)
    db.commit()
    db.refresh(db_quizquestion)
    return db_quizquestion


def delete(db: Session, quizquestion_id: int ) -> None:
    """delete the quizquestion object if found, else raise an exception."""

    db_quizquestion = db.query(QuizQuestion).get(quizquestion_id)
    # throw an exception if not found
    if not db_quizquestion:
        raise NotFoundException(
            msg=f"quizquestion with id {quizquestion_id} doesn't exist"
        )
    db.delete(db_quizquestion)
    db.commit()
