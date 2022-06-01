from fnmatch import translate
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class TranslationBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored translation Id in the backend."
    )
    language_id: int = Field(
        title="The language_id of the translation",
    )
    translation: str = Field(
        title="The translation of the word",
    )
    created: datetime = Field(
        title="The datetime of the creation of the translation record in the backend."
    )
    
    class Config:
        orm_mode = True


class TranslationInsert(BaseModel):
    """use for the insert operations"""

    language_id: int = Field(
        title="The language_id of the translation",
    )

    translation: str = Field(
        title="The translation of the word",
        max_length=255
    )


class TranslationUpdate(BaseModel):
    """use for the update operations"""


    language_id: Optional[int] = Field(
        title="The language_id of the translation",
    )

    translation: Optional[str] = Field(
        title="The translation of the word",
        max_length=255
    )


class TranslationCustomResponse(BaseModel):
    """use for the update operations"""

    translation: str
    language_name: str

    class Config:
        orm_mode = True


class PaginatedTranslationInfo(BaseModel):
    limit: int
    offset: int
    data: List[TranslationBase]
