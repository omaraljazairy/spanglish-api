from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class WordBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored word Id in the backend."
    )
    text: str = Field(
        title="The text in Spanish for this application.",
    )
    category_id: int = Field(
        title="The category id that belongs to it",
    )
    created: datetime = Field(
        title="The datetime of the creation of the language record in the backend."
    )
    
    class Config:
        orm_mode = True


class WordInsert(BaseModel):
    """use for the insert operations"""

    text: str = Field(
        title="The Spanish word",
        max_length=15
    )

    category_id: int = Field(
        title="The category_id",
    )


class WordUpdate(BaseModel):
    """use for the insert and update operations"""

    text: Optional[str] = Field(
        title="The Spanish word",
        max_length=15
    )
    category_id: Optional[int] = Field(
        title="The category_id",
    )


class PaginatedWordInfo(BaseModel):
    limit: int
    offset: int
    data: List[WordBase]
