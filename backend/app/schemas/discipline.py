from typing import Optional

from pydantic import BaseModel


class DisciplineBase(BaseModel):
    title: str


# Properties to receive via API on creation
class DisciplineCreate(DisciplineBase):
    pass


# Properties to receive via API on update
class DisciplineUpdate(DisciplineBase):
    pass


class DisciplineInDBBase(DisciplineBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class DisciplineInDB(DisciplineInDBBase):
    pass


# Additional properties to return via API
class Discipline(DisciplineInDBBase):
    pass
