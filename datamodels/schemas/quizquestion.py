from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


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
    created: datetime = Field(
        title="The datetime of the creation of the quizquestion record in the backend."
    )
    
    class Config:
        orm_mode = True


class QuizQuestionInsert(BaseModel):
    """use for the insert operations"""

    word_id: int
    quiz_id: int
    question: Optional[str] = Field(
        title="The question that can be presented for the word_id.",
        max_length=255,
        default='What is the meaning of'
    )


class QuizQuestionUpdate(BaseModel):
    """use for the update operations"""

    word_id: Optional[int]
    quiz_id: Optional[int]
    question: Optional[str]


class PaginatedQuizQuestionInfo(BaseModel):
    limit: int
    offset: int
    data: List[QuizQuestionBase]
