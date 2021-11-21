from settings import discounts, fines, except_options
from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import DeerUsage, Fee
from src.rate_policies.domain.models.policies import BasicRatePolicy, AmountDiscountPolicy, RateDiscountPolicy, \
    FinePolicy, ExceptionPolicy


class FeeCalculator:
    def __init__(self, uow: AbstractCalculatorUnitOfWork):
        self.uow = uow

    def calculate_with(self, usage: DeerUsage):
        area_fee = self.uow.area_fees.get_fee_of(usage.use_deer.deer_area.area_id)
        basic_policy = BasicRatePolicy(usage=usage, area_fee=area_fee)
        rate_discount_policy = RateDiscountPolicy(usage=usage, area_fee=area_fee, uow=self.uow, options=discounts)
        amount_discount_policy = AmountDiscountPolicy(usage=usage, area_fee=area_fee, uow=self.uow, options=discounts)
        fine_policy = FinePolicy(usage=usage, area_fee=area_fee, uow=self.uow, options=fines)
        exception_policy = ExceptionPolicy(usage=usage, area_fee=area_fee, options=except_options, uow=self.uow)

        return exception_policy.apply_on(
            fine_policy.apply_on(
                amount_discount_policy.apply_on(
                    rate_discount_policy.apply_on(
                        basic_policy.apply_on(Fee(amount=0, currency=area_fee.base.currency))
                    )
                )
            )
        )
