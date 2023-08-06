from typing import Optional

from bson import ObjectId  # type: ignore
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class Model(PydanticBaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")

    class Config:
        arbitrary_types_allowed = True
        extra = "ignore"
        allow_population_by_field_name = True
