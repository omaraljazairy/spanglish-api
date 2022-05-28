from sqlalchemy.orm import Session
from datamodels.models import QuizResult, QuizQuestion, User
from datamodels.schemas.quizresult import QuizResultInsert, QuizResultUpdate
from exceptions.model_exceptions import NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_quizresults(db: Session):
    """return all data from the quizresult model."""

    return db.query(QuizResult).all()


def create(db: Session, request: QuizResultInsert):
    """create a new QuizResult object."""

    # check if the question exists, throw an exception if not
    existing_quizquestion = db.query(QuizQuestion).filter(
    QuizQuestion.id == request.quizquestion_id
    ).first()

    if not existing_quizquestion:
        logger.error(f"non existing_quizquestion => {request.quizquestion_id}")
        raise NotFoundException(
            msg=f"QuizQuestion with id {request.quizquestion_id} does not exists"
        )

    # check if the user exists, throw an exception if not
    existing_user = db.query(User).filter(
    User.id == request.user_id
    ).first()

    if not existing_user:
        logger.error(f"non existing_user => {request.user_id}")
        raise NotFoundException(
            msg=f"User with id {request.user_id} does not exists"
        )

    db_quizresult = QuizResult(
        **request.dict()
    )
    db.add(db_quizresult)
    db.commit()
    db.refresh(db_quizresult)
    return db_quizresult


def update(db: Session, request: QuizResultUpdate, quizresult_id: int):
    """
    update the quizresult model. take the QuizResultUpdate schema and a 
    quizresult_id as params. returns a quizresult object.
    """
    db_quizresult = db.query(QuizResult).get(quizresult_id)
    # throw an exception if not found
    if not db_quizresult:
        raise NotFoundException(
            msg=f"quizresult with id {quizresult_id} is not found"
        )
    
    requested_quizresult = request.dict(exclude_unset=True)
    for key, value in requested_quizresult.items():
        setattr(db_quizresult, key, value)
    db.add(db_quizresult)
    db.commit()
    db.refresh(db_quizresult)
    return db_quizresult


def delete(db: Session, quizresult_id: int ) -> None:
    """delete the quizresult object if found, else raise an exception."""

    db_quizresult = db.query(QuizResult).get(quizresult_id)
    # throw an exception if not found
    if not db_quizresult:
        raise NotFoundException(
            msg=f"quizresult with id {quizresult_id} doesn't exist"
        )
    db.delete(db_quizresult)
    db.commit()
