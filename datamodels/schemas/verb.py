from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class VerbBase(BaseModel):
    """ base response model used for the api. It contains all the fields."""
    
    id: int = Field(
        title="The stored word Id in the backend."
    )
    word_id: int = Field(
        title="The word id in Spanish that the verb belongs to.",
    )
    yo: str = Field(
        title="The verb for the subject pronouns yo",
    )
    tu: str = Field(
        title="The verb for the subject pronouns tu",
    )
    el_ella_usted: str = Field(
        title="The verb for the subject pronouns el_ella_usted",
    )
    nosotros: str = Field(
        title="The verb for the subject pronouns nosotros",
    )
    vosotros: str = Field(
        title="The verb for the subject pronouns vosotros",
    )
    ellos_ellas_ustedes: str = Field(
        title="The verb for the subject pronouns ellos_ellas_ustedes",
    )                    
    created: datetime = Field(
        title="The datetime of the creation of the verb record in the backend."
    )
    
    class Config:
        orm_mode = True


class VerbInsert(BaseModel):
    """use for the insert operations"""

    word_id: int = Field(
        title="The word id in Spanish that the verb belongs to.",
    )
    yo: Optional[str] = Field(
        title="The verb for the subject pronouns yo",
    )
    tu: Optional[str] = Field(
        title="The verb for the subject pronouns tu",
    )
    el_ella_usted: Optional[str] = Field(
        title="The verb for the subject pronouns el_ella_usted",
    )
    nosotros: Optional[str] = Field(
        title="The verb for the subject pronouns nosotros",
    )
    vosotros: Optional[str] = Field(
        title="The verb for the subject pronouns vosotros",
    )
    ellos_ellas_ustedes: Optional[str] = Field(
        title="The verb for the subject pronouns ellos_ellas_ustedes",
    )

class VerbUpdate(BaseModel):
    """use for the update operations"""

    word_id: Optional[int] = Field(
        title="The word id in Spanish that the verb belongs to.",
    )
    yo: Optional[str] = Field(
        title="The verb for the subject pronouns yo",
    )
    tu: Optional[str] = Field(
        title="The verb for the subject pronouns tu",
    )
    el_ella_usted: Optional[str] = Field(
        title="The verb for the subject pronouns el_ella_usted",
    )
    nosotros: Optional[str] = Field(
        title="The verb for the subject pronouns nosotros",
    )
    vosotros: Optional[str] = Field(
        title="The verb for the subject pronouns vosotros",
    )
    ellos_ellas_ustedes: Optional[str] = Field(
        title="The verb for the subject pronouns ellos_ellas_ustedes",
    )

class PaginatedVerbInfo(BaseModel):
    limit: int
    offset: int
    data: List[VerbBase]
