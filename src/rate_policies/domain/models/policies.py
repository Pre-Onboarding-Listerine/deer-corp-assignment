import abc
from typing import List

from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import Fee, DeerUsage, AreaFee
from src.rate_policies.domain.models.statements import ParkingZoneStatement, ReuseStatement, \
    AmountDiscountStatement, RateDiscountStatement


class Policy(abc.ABC):
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
        self.statements: List[AmountDiscountStatement] = [
            ReuseStatement(discount_amount=area_fee.base.amount, options=options["reuse"], usages=uow.usages),
        ]

    def apply_on(self, fee: Fee) -> Fee:
        max_amount = 0
        used_currency = fee.currency
        for statement in self.statements:
            if statement.is_available_currency(used_currency) and statement.is_applicable(self.usage):
                max_amount = statement.discount_amount
        return fee - Fee(amount=max_amount, currency=used_currency)


class RateDiscountPolicy(Policy):
    def __init__(self, usage: DeerUsage, area_fee: AreaFee, uow: AbstractCalculatorUnitOfWork, options: dict):
        super().__init__(usage, area_fee)
        self.statements: List[RateDiscountStatement] = [
            ParkingZoneStatement(discount_rate=options["parking_zone"]["rate"], parking_zones=uow.parking_zones),
        ]

    def apply_on(self, fee: Fee) -> Fee:
        max_rate = 0
        for statement in self.statements:
            if statement.is_applicable(self.usage):
                max_rate = statement.discount_rate / 100
        return fee * (1 - max_rate)


class FinePolicy(Policy):
    def apply_on(self, fee: Fee) -> Fee:
        pass
