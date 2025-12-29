from pydantic import BaseModel, Field


class BaseItemSchema(BaseModel):
    full_name: str = Field(validation_alias="fullname")
    name: str
    id: int = Field(validation_alias="value")
