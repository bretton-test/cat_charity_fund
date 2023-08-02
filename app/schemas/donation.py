from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDbAdmin(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int
