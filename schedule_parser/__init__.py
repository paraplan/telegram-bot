from pydantic import BaseModel, Field


class BaseItem(BaseModel):
    id: str = Field(validation_alias="value")
    name: str
    full_name: str = Field(validation_alias="fullname")
