import abc
from typing import List

from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import Fee, DeerUsage, AreaFee
from src.rate_policies.domain.models.articles import ParkingZoneArticle, ReuseArticle, Article, OutOfReturnAreaArticle, \
    ForbiddenReturnAreaArticle, BrokenDeerArticle


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
    def __init__(self, usage: DeerUsage, area_fee: AreaFee, uow: AbstractCalculatorUnitOfWork, options: dict):
        super().__init__(usage, area_fee)
        self.articles = [
            OutOfReturnAreaArticle(
                fine_rate=options["out_of_return_area"]["rate_per_meter"],
                options=options["out_of_return_area"],
                areas=uow.areas
            ),
            ForbiddenReturnAreaArticle(
                fine_amount=options["forbidden_return_area"]["amount"],
                options=options["forbidden_return_area"],
                forbidden_areas=uow.forbidden_areas
            )
        ]

    def apply_on(self, fee: Fee) -> Fee:
        fined_fee = fee
        for article in self.articles:
            fined_fee = article.calculate(fined_fee, self.usage)
        return fined_fee


class ExceptionPolicy(Policy):
    def __init__(self, usage: DeerUsage, area_fee: AreaFee, uow: AbstractCalculatorUnitOfWork, options: dict):
        super().__init__(usage, area_fee)
        self.articles = [
            BrokenDeerArticle(options=options["broken_deer"])
        ]

    def apply_on(self, fee: Fee) -> Fee:
        final_fee = fee
        for article in self.articles:
            final_fee = article.calculate(final_fee, self.usage)
        return final_fee
