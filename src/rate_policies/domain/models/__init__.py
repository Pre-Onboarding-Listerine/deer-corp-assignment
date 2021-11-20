from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel

from src.rate_policies.exceptions import DifferentCurrencyException, DifferentTypeAddOperationException


class Location(BaseModel):
    lat: float
    lng: float


class Fee(BaseModel):
    amount: float
    currency: str

    def __add__(self, other: Fee):
        if not isinstance(other, Fee):
            raise DifferentTypeAddOperationException(f"{type(other)} type is different from {type(Fee)} type")
        if self.currency == other.currency:
            new_amount = self.amount + other.amount
            return Fee(amount=new_amount, currency=self.currency)
        else:
            raise DifferentCurrencyException(f"{other.currency} is different from {self.currency}")

    def __sub__(self, other: Fee):
        if not isinstance(other, Fee):
            raise DifferentTypeAddOperationException(f"{type(other)} type is different from {type(Fee)} type")
        if self.currency == other.currency:
            new_amount = self.amount - other.amount
            if new_amount < 0:
                return Fee(amount=0, currency=self.currency)
            return Fee(amount=new_amount, currency=self.currency)
        else:
            raise DifferentCurrencyException(f"{other.currency} is different from {self.currency}")

    def __mul__(self, other: float):
        new_amount = self.amount * other
        return Fee(amount=new_amount, currency=self.currency)


class UsageTime(BaseModel):
    start: datetime
    end: datetime

    @property
    def duration(self):
        duration = self.end - self.start
        return duration.total_seconds() / 60


class Usage(BaseModel):
    user_id: int
    use_deer_name: str
    end_location: Location
    usage_time: UsageTime

    @property
    def minutes(self) -> float:
        return self.usage_time.duration
