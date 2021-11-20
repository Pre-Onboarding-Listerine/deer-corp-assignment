from datetime import datetime

import pytest
from assertpy import assert_that

from src.configs.discount_options import PARKING_ZONE_ARTICLE, REUSE_ARTICLE
from src.rate_policies.domain.models import Fee, DeerUsage, UsageTime, AreaFee, Deer
from src.rate_policies.domain.models.areas import Location
from src.rate_policies.domain.models.policies import AmountDiscountPolicy
from tests.unit.fixtures.unit_of_work import FakeCalculatorUnitOfWork, FakeUsageRepository


class TestAmountDiscountPolicy:
    @pytest.fixture
    def calculator_uow(self):
        uow = FakeCalculatorUnitOfWork()
        uow.usages = FakeUsageRepository({
            1: DeerUsage(
                user_id=1,
                use_deer=Deer(deer_name="deer-1", deer_area_id=1),
                end_location=Location(
                    lat=37.541983,
                    lng=127.078179
                ),
                usage_time=UsageTime(
                    start=datetime(2021, 11, 18, 8, 20, 0),
                    end=datetime(2021, 11, 18, 8, 50, 0)
                )
            )
        })
        return uow

    @pytest.fixture
    def amount_discount_policy(self):
        return AmountDiscountPolicy

    class TestCalculate:

        class TestInKunKukUniv:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.541983,
                    lng=127.078179
                )

            @pytest.fixture
            def area_fee(self):
                return AreaFee(
                    area_id=1,
                    base=Fee(amount=790, currency="KRW"),
                    rate_per_minute=Fee(amount=150, currency="KRW")
                )

            class TestWithUse10Minutes:
                @pytest.fixture
                def usage_time(self):
                    return UsageTime(
                        start=datetime(2021, 11, 18, 9, 0, 0),
                        end=datetime(2021, 11, 18, 9, 10, 0)
                    )

                @pytest.fixture
                def usage(self, end_location, usage_time):
                    return DeerUsage(
                        user_id=1,
                        use_deer=Deer(deer_name="deer-1", deer_area_id=1),
                        end_location=end_location,
                        usage_time=usage_time
                    )

                @pytest.fixture
                def policy(self, amount_discount_policy, usage, area_fee, calculator_uow):
                    options = {
                        "parking_zone": PARKING_ZONE_ARTICLE,
                        "reuse": REUSE_ARTICLE
                    }
                    return amount_discount_policy(usage, area_fee, calculator_uow, options)

                def test_it_returns_basic_fee(self, policy, area_fee):
                    basic_fee = Fee(amount=2290, currency="KRW")
                    rate_discounted_fee = policy.apply_on(basic_fee)
                    expected = basic_fee - area_fee.base

                    assert_that(rate_discounted_fee).is_equal_to(expected)

