from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class QuizBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored quiz Id in the backend."
    )
    title: str = Field(
        title="The title of the quiz.",
        max_length=30
    )
    active: bool = Field(
        title="If True, the quiz is active, else False",
        default=1
    )
    created: datetime = Field(
        title="The datetime of the creation of the quiz record in the backend."
    )
    
    class Config:
        orm_mode = True


class QuizCustomResponse(BaseModel):
    """custom response for the quizquestions."""

    id: int = Field(
        title="The stored quiz Id in the backend."
    )
    title: str = Field(
        title="The title of the quiz.",
        max_length=30
    )
    active: bool = Field(
        title="If True, the quiz is active, else False",
        default=1
    )

    class Config:
        orm_mode = True


class QuizInsert(BaseModel):
    """use for the insert operations"""

    title: str = Field(
        title="The title of the quiz.",
        max_length=30
    )
    active: Optional[bool] = Field(
        title="If 1, the quiz is active, else 0 not active. default is 1",
        default=1
    )


class QuizUpdate(BaseModel):
    """use for the update operations"""

    title: Optional[str] = Field(
        title="The title of the quiz.",
        max_length=30
    )
    active: Optional[bool] = Field(
        title="If 1, the quiz is active, else 0 not active. default is 1",
        default=1
    )


class PaginatedQuizInfo(BaseModel):
    limit: int
    offset: int
    data: List[QuizBase]
