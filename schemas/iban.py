from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class IbanBase(BaseModel):
    class Config:
        orm_mode = True


class IbanCreate(IbanBase):
    iban: str


class Iban(IbanBase):
    id: UUID
    iban: str
    status: str
    created_at: datetime
