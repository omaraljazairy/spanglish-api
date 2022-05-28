from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class QuizResultBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored quizresult Id in the backend."
    )
    quizquestion_id: int = Field(
        title="The Id of the quizquestion id that is related to the answer."
    )
    attempts: int = Field(
        title="The number of attempts to get the correct answer.",
        description="example: 2 means from the 2nd attempt."
    )
    user_id: int = Field(
        title="The user_id of the user who is taking the quiz.",
    )
    created: datetime = Field(
        title="The datetime of the creation of the quizresult record in the backend."
    )
    
    class Config:
        orm_mode = True


class QuizResultInsert(BaseModel):
    """use for the insert operations"""

    quizquestion_id: int
    attempts: int
    user_id: int


class QuizResultUpdate(BaseModel):
    """use for the update operations"""

    quizquestion_id: Optional[int]
    attempts: Optional[int]
    user_id: Optional[int]


class PaginatedQuizResultInfo(BaseModel):
    limit: int
    offset: int
    data: List[QuizResultBase]
