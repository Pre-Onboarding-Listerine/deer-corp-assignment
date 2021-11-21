import abc
from typing import List

from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import Fee, DeerUsage, AreaFee
from src.rate_policies.domain.models.articles import ParkingZoneArticle, ReuseArticle, Article


class Policy(abc.ABC):
    articles: List[Article]

    def __init__(self, usage: DeerUsage, area_fee: AreaFee):
        self.usage = usage
        self.area_fee = area_fee

    @abc.abstractmethod
    def apply_on(self, fee: Fee) -> Fee:
        raise NotImplementedError


class BasicRatePolicy(Policy):
    def __init__(self, usage: DeerUsage, area_fee: AreaFee):
        super().__init__(usage, area_fee)

    def apply_on(self, fee: Fee) -> Fee:
        return fee + self.area_fee.base + self.area_fee.rate_per_minute * self.usage.minutes


class AmountDiscountPolicy(Policy):
    def __init__(self, usage: DeerUsage, area_fee: AreaFee, uow: AbstractCalculatorUnitOfWork, options: dict):
        super().__init__(usage, area_fee)
        self.articles = [
            ReuseArticle(discount_amount=area_fee.base.amount, options=options["reuse"], usages=uow.usages),
        ]

    def apply_on(self, fee: Fee) -> Fee:
        min_fee = fee
        for article in self.articles:
            new_fee = article.calculate(fee, self.usage)
            if min_fee > new_fee:
                min_fee = new_fee
        return min_fee


class RateDiscountPolicy(Policy):
    def __init__(self, usage: DeerUsage, area_fee: AreaFee, uow: AbstractCalculatorUnitOfWork, options: dict):
        super().__init__(usage, area_fee)
        self.articles = [
            ParkingZoneArticle(discount_rate=options["parking_zone"]["rate"], parking_zones=uow.parking_zones),
        ]

    def apply_on(self, fee: Fee) -> Fee:
        min_fee = fee
        for article in self.articles:
            new_fee = article.calculate(fee, self.usage)
            if min_fee > new_fee:
                min_fee = new_fee
        return min_fee


class FinePolicy(Policy):
    def apply_on(self, fee: Fee) -> Fee:
        pass
