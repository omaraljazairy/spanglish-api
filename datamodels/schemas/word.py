from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union

from datamodels.schemas.translation import TranslationBase, TranslationInsert, TranslationCustomResponse
from datamodels.schemas.verb import VerbWordResponse


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

    translations: List[TranslationBase]
    verb_pronounces: Union[VerbWordResponse, dict]
    
    class Config:
        orm_mode = True


class WordVerb(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored word Id in the backend."
    )
    text: str = Field(
        title="The text in Spanish for this application.",
    )
    category_name: str = Field(
        title="The category id that belongs to it",
    )

    translations: List[TranslationCustomResponse]
    verb_pronounces: Union[VerbWordResponse, dict]
    
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
    user_id: int = Field(
        title="The user_id",
    )

    translations: List[TranslationInsert]

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
    translations: List[TranslationCustomResponse]

    class Config:
        orm_mode = True


class PaginatedWordInfo(BaseModel):
    limit: int
    offset: int
    data: List[WordBase]
