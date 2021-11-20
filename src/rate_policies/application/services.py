from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import DeerUsage, Fee
from src.rate_policies.domain.models.calculator import FeeCalculator


class FeeCalculatorClient:
    def __init__(self, uow: AbstractCalculatorUnitOfWork):
        self.uow = uow

    def get_fee(self, usage: DeerUsage) -> Fee:
        with self.uow:
            calculator = FeeCalculator.of(user_id=usage.user_id)
            return calculator.calculate_with(usage)
