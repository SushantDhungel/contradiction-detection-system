from sqlmodel import SQLModel, Field
from pydantic import BaseMo

class Text(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    input_text: str

class TextResponse()

# TODO: Maybe we will be tokeninizing the texts
