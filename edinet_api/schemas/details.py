from typing import Optional
from pydantic import BaseModel, Field


class DetailBase(BaseModel):
    pass


class DetailCreate(DetailBase):
    # action: str= Field(None, example="fetch")
    # date: int= Field(None, example="20230111")
    pass

class DetailCreateResponse(DetailCreate):
    pass
    class Config:
        orm_mode = True


class Detail(DetailBase):
    pass

    class Config:
        orm_mode = False
