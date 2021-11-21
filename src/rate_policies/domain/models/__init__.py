from __future__ import annotations
from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel

from src.rate_policies.domain.models.areas import Location, Area
from src.rate_policies.exceptions import DifferentCurrencyException, DifferentTypeOperationException


class Fee(BaseModel):
    amount: float
    currency: str
    applied_articles: Dict = dict()

    def __gt__(self, other):
        if not isinstance(other, Fee):
            raise DifferentTypeOperationException(f"{type(other)} type is different from {type(Fee)} type")
        if self.currency != other.currency:
            raise DifferentCurrencyException(f"{other.currency} is different from {self.currency}")
        return self.amount > other.amount

    def __le__(self, other):
        return not self.__gt__(other)

    def __add__(self, other: Fee):
        if not isinstance(other, Fee):
            raise DifferentTypeOperationException(f"{type(other)} type is different from {type(Fee)} type")
        if self.currency == other.currency:
            new_amount = self.amount + other.amount
            return Fee(amount=new_amount, currency=self.currency)
        else:
            raise DifferentCurrencyException(f"{other.currency} is different from {self.currency}")

    def __sub__(self, other: Fee):
        if not isinstance(other, Fee):
            raise DifferentTypeOperationException(f"{type(other)} type is different from {type(Fee)} type")
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


class AreaFee(BaseModel):
    area_id: int
    base: Fee
    rate_per_minute: Fee


class UsageTime(BaseModel):
    start: datetime
    end: datetime

    @property
    def duration(self):
        duration = self.end - self.start
        return duration.total_seconds() / 60


class Deer(BaseModel):
    deer_name: int
    deer_area: Area

    class Config:
        orm_mode = True


class DeerUsage(BaseModel):
    user_id: int
    use_deer: Deer
    end_location: Location
    usage_time: UsageTime

    class Config:
        orm_mode = True

    @property
    def minutes(self) -> float:
        return self.usage_time.duration
