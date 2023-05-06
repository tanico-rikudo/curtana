from typing import Optional
from pydantic import BaseModel, Field


class HeadlineBase(BaseModel):
    pass


class HeadlineCreate(HeadlineBase):
    action: str= Field(None, example="fetch")
    date: int= Field(None, example="20230111")


class HeadlineCreateResponse(HeadlineCreate):
    pass
    class Config:
        orm_mode = True


class Headline(HeadlineBase):
    pass

    class Config:
        orm_mode = False
