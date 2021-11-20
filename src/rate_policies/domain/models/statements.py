import abc
from datetime import timedelta

from src.rate_policies.domain.models import DeerUsage, Fee
from src.rate_policies.domain.models.areas import ParkingZone
from src.rate_policies.infra.parking_zone_repository import AbstractParkingZoneRepository
from src.rate_policies.infra.usage_repository import AbstractUsageRepository


class Statement(abc.ABC):
    usage: DeerUsage

    @abc.abstractmethod
    def is_applicable(self, usage: DeerUsage) -> bool:
        raise NotImplementedError


class RateDiscountStatement(Statement):
    discount_rate: float

    @abc.abstractmethod
    def is_applicable(self, usage: DeerUsage) -> bool:
        raise NotImplementedError


class AmountDiscountStatement(Statement):
    discount_amount: float
    currency: str

    @abc.abstractmethod
    def is_applicable(self, usage: DeerUsage) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def is_available_currency(self, user_currency: str):
        raise NotImplementedError


class ParkingZoneStatement(RateDiscountStatement):
    def __init__(self, discount_rate: float, parking_zones: AbstractParkingZoneRepository):
        self.discount_rate = discount_rate
        self.parking_zones = parking_zones

    def is_applicable(self, usage: DeerUsage) -> bool:
        available_zones = self.parking_zones.locate_in(usage.use_deer.deer_area_id)
        for zone in available_zones:
            if zone.includes(usage.end_location):
                return True
        return False


class ReuseStatement(AmountDiscountStatement):
    def __init__(self, discount_amount: float, options: dict, usages: AbstractUsageRepository):
        self.discount_amount = discount_amount
        self.currency = options["currency"]
        self.limit = timedelta(minutes=options["minutes"])
        self.usages = usages

    def is_applicable(self, usage: DeerUsage) -> bool:
        last_usage = self.usages.get_right_before_usage(user_id=usage.user_id)
        if last_usage.use_deer.deer_name != usage.use_deer.deer_name:
            return False
        reuse_delta = usage.usage_time.start - last_usage.usage_time.end
        if self.limit < reuse_delta:
            return False
        return True

    def is_available_currency(self, user_currency: str):
        if self.currency == user_currency:
            return True
        else:
            return False
