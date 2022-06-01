from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from datamodels.schemas.translation import TranslationBase, TranslationInsert, TranslationCustomResponse


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
        title="The datetime of the creation of the word record in the backend."
    )

    translation: List[TranslationBase]
    
    class Config:
        orm_mode = True


class WordInsert(BaseModel):
    """use for the insert operations"""

    text: str = Field(
        title="The Spanish word",
        max_length=255
    )

    category_id: int = Field(
        title="The category_id",
    )

    translation: List[TranslationInsert]

    class Config:
        arbitrary_types_allowed = True


class WordUpdate(BaseModel):
    """use for the update operations"""

    text: Optional[str] = Field(
        title="The Spanish text of word or sentence",
        max_length=255
    )
    category_id: Optional[int] = Field(
        title="The category_id",
    )


class WordWithTranslationResponse(BaseModel):
    """returns the translation with the word."""

    id: int
    text: str
    category_name: str
    translation: List[TranslationCustomResponse]

    class Config:
        orm_mode = True


class PaginatedWordInfo(BaseModel):
    limit: int
    offset: int
    data: List[WordBase]
