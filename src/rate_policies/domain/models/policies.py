import abc
from typing import List

from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import Fee, DeerUsage, AreaFee
from src.rate_policies.domain.models.statements import Statement, ParkingZoneStatement, ReuseStatement


class Policy(abc.ABC):
    statements: List[Statement]

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
        self.statements = [
            ReuseStatement(discount_amount=area_fee.base.amount, options=options["reuse"], usages=uow.usages),
        ]

    def apply_on(self, fee: Fee) -> Fee:
        max_amount = 0
        for statement in self.statements:
            if statement.is_applicable(self.usage):
                max_amount = statement.discount_value
        return fee - Fee(amount=max_amount, currency=self.area_fee.base.currency)


class RateDiscountPolicy(Policy):
    def __init__(self, usage: DeerUsage, area_fee: AreaFee, uow: AbstractCalculatorUnitOfWork, options: dict):
        super().__init__(usage, area_fee)
        self.statements = [
            ParkingZoneStatement(discount_rate=options["parking_zone"]["rate"], parking_zones=uow.parking_zones),
        ]

    def apply_on(self, fee: Fee) -> Fee:
        max_rate = 0
        for statement in self.statements:
            if statement.is_applicable(self.usage):
                max_rate = statement.discount_value / 100
        return fee * (1 - max_rate)


class FinePolicy(Policy):
    def apply_on(self, fee: Fee) -> Fee:
        pass
