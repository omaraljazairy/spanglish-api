from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from datamodels.schemas.word import WordVerb
from datamodels.schemas.quiz import QuizCustomResponse

class QuizQuestionBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored quizquestion Id in the backend."
    )
    word_id: int = Field(
        title="The Id of the word of the answer to the quizquestion."
    )
    quiz_id: int = Field(
        title="The quiz where this quizquestion belongs to"
    )
    question: str = Field(
        title="The question that can be presented for the word_id.",
        max_length=255,
        default='What is the meaning of'
    )
    active: bool = Field(
        title="makes the question active or inactive",
        default=True
    )
    created: datetime = Field(
        title="The datetime of the creation of the quizquestion record in the backend."
    )
    updated: datetime = Field(
        title="The datetime of the update of the quizquestion record in the backend."
    )
    
    class Config:
        orm_mode = True


class QuizQuestionDetails(BaseModel):
    """ response model used for the api to give details about a single quizquestion."""
    
    id: int
    word: WordVerb
    question_quiz: QuizCustomResponse
    question: str
    active: bool
    
    class Config:
        orm_mode = True


class QuizQuestionInsert(BaseModel):
    """use for the insert operations"""

    word_id: int
    quiz_id: int
    question: Optional[str]
    active: bool = True


class QuizQuestionUpdate(BaseModel):
    """use for the update operations"""

    word_id: Optional[int]
    quiz_id: Optional[int]
    question: Optional[str]
    active: Optional[bool]
    updated: datetime = datetime.now()


class PaginatedQuizQuestionInfo(BaseModel):
    limit: int
    offset: int
    data: List[QuizQuestionBase]
