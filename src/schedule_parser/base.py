from pydantic import BaseModel, Field


class BaseItem(BaseModel):
    full_name: str = Field(validation_alias="fullname")
    name: str
    id: int = Field(validation_alias="value")
