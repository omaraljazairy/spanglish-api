from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class TranslationBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored translation Id in the backend."
    )
    word_id: int = Field(
        title="The word_id of the spanish text.",
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

    word_id: int = Field(
        title="The Spanish word_id"
    )

    language_id: int = Field(
        title="The language_id of the translation",
    )

    translation: str = Field(
        title="The translation of the word",
        max_length=255
    )


class TranslationUpdate(BaseModel):
    """use for the update operations"""

    word_id: Optional[int] = Field(
        title="The Spanish word_id"
    )

    language_id: Optional[int] = Field(
        title="The language_id of the translation",
    )

    translation: Optional[str] = Field(
        title="The translation of the word",
        max_length=255
    )


class PaginatedTranslationInfo(BaseModel):
    limit: int
    offset: int
    data: List[TranslationBase]
