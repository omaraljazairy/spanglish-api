from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class LanguageBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored language Id in the backend."
    )
    name: str = Field(
        title="The name of the language. ex: `English`.",
    )
    code: str = Field(
        title="The ISO 639-2 language code. ex: `EN`",
    )
    created: datetime = Field(
        title="The datetime of the creation of the language record in the backend."
    )
    
    class Config:
        orm_mode = True


class LanguageInsert(BaseModel):
    """use for the insert operations"""

    name: str = Field(
        title="The of the language. ex: `English`.",
        max_length=15,
        min_length=5
    )
    code: str = Field(
        title="The ISO 639-2 language code. ex: `EN`",
        max_length=2,
        min_length=2
    )


class LanguageUpdate(BaseModel):
    """use for the insert and update operations"""

    name: Optional[str] = Field(
        title="The of the language. ex: `English`.",
        max_length=15
    )
    code: Optional[str] = Field(
        title="The ISO 639-2 language code. ex: `EN`",
        max_length=2
    )


class PaginatedLanguageInfo(BaseModel):
    limit: int
    offset: int
    data: List[LanguageBase]