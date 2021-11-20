from datetime import datetime

import pytest
from assertpy import assert_that

from src.rate_policies.domain.models import Fee, DeerUsage, UsageTime, AreaFee, Deer
from src.rate_policies.domain.models.areas import Location
from src.rate_policies.domain.models.policies import BasicRatePolicy


class TestBasicRatePolicy:
    @pytest.fixture
    def basic_rate_policy(self):
        return BasicRatePolicy

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
                def policy(self, basic_rate_policy, usage, area_fee):
                    return basic_rate_policy(usage, area_fee)

                def test_it_returns_basic_fee(self, policy, area_fee):
                    basic_fee = policy.apply_on(Fee(amount=0, currency="KRW"))
                    usage_minutes = policy.usage.minutes
                    expected = area_fee.base + area_fee.rate_per_minute * usage_minutes

                    assert_that(basic_fee).is_equal_to(expected)
