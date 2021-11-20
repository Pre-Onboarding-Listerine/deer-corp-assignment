import abc
from datetime import timedelta

from src.rate_policies.domain.models import Usage, Fee
from src.rate_policies.domain.models.areas import ParkingZone


class Statement(abc.ABC):
    usage: Usage

    @abc.abstractmethod
    def is_applicable(self, usage: Usage) -> bool:
        raise NotImplementedError


class RateDiscountStatement(Statement):
    discount_rate: float

    @abc.abstractmethod
    def is_applicable(self, usage: Usage) -> bool:
        raise NotImplementedError


class AmountDiscountStatement(Statement):
    amount: Fee

    @abc.abstractmethod
    def is_applicable(self, usage: Usage) -> bool:
        raise NotImplementedError


class ParkingZoneStatement(RateDiscountStatement):
    def __init__(self, discount_rate: float, parking_zone: ParkingZone):
        self.discount_rate = discount_rate
        self.parking_zone = parking_zone

    def is_applicable(self, usage: Usage) -> bool:
        if self.parking_zone.includes(usage.end_location):
            return True
        else:
            return False


class ReuseStatement(AmountDiscountStatement):
    def __init__(self, limit: int, last_usage: Usage):
        self.limit = timedelta(minutes=limit)
        self.last_usage = last_usage

    def is_applicable(self, usage: Usage) -> bool:
        if self.last_usage.use_deer_name != usage.use_deer_name:
            return False
        reuse_delta = usage.usage_time.start - self.last_usage.usage_time.end
        if self.limit < reuse_delta:
            return False
        return True
