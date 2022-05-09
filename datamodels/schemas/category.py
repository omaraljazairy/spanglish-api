from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class CategoryBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored category Id in the backend."
    )
    name: str = Field(
        title="The name of the category. ex: `Verb`.",
    )
    created: datetime = Field(
        title="The datetime of the creation of the category record in the backend."
    )
    
    class Config:
        orm_mode = True


class CategoryInsertUpdate(BaseModel):
    """use for the insert and update operations"""

    name: str = Field(
        title="The name of the category. ex: `Verb`.",
        max_length=15
    )


class PaginatedCategoryInfo(BaseModel):
    limit: int
    offset: int
    data: List[CategoryBase]
