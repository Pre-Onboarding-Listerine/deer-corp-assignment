from datetime import datetime

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon

from src.configs.discount_options import PARKING_ZONE_ARTICLE, REUSE_ARTICLE
from src.rate_policies.domain.models import Fee, DeerUsage, UsageTime, AreaFee, Deer, areas
from src.rate_policies.domain.models.areas import Location, ParkingZone
from src.rate_policies.domain.models.policies import RateDiscountPolicy
from tests.unit.fixtures.unit_of_work import FakeCalculatorUnitOfWork, FakeParkingZoneRepository


class TestRateDiscountPolicy:
    @pytest.fixture
    def deer_area(self):
        return areas.Area(
            area_id=1,
            area_boundary=Polygon(coordinates=[
                [(37.543272, 127.07655), (37.541734, 127.074072), (37.539088, 127.07449), (37.538928, 127.078034),
                 (37.540417, 127.080781), (37.542416, 127.080599), (37.543272, 127.07655)]]),
            area_center=Location(lat=37.541302, lng=127.077852),
        )

    @pytest.fixture
    def calculator_uow(self):
        uow = FakeCalculatorUnitOfWork()
        uow.parking_zones = FakeParkingZoneRepository({
            1: [
                ParkingZone(
                    parkingzone_id=1,
                    parkingzone_center=Location(lat=37.541732, lng=127.079799),
                    parkingzone_radius=200
                )
            ]
        })
        return uow

    @pytest.fixture
    def rate_discount_policy(self):
        return RateDiscountPolicy

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
                def usage(self, deer_area, end_location, usage_time):
                    return DeerUsage(
                        user_id=1,
                        use_deer=Deer(deer_name=1, deer_area=deer_area),
                        end_location=end_location,
                        usage_time=usage_time
                    )

                @pytest.fixture
                def policy(self, rate_discount_policy, usage, area_fee, calculator_uow):
                    options = {
                        "parking_zone": PARKING_ZONE_ARTICLE,
                        "reuse": REUSE_ARTICLE
                    }
                    return rate_discount_policy(usage, area_fee, calculator_uow, options)

                def test_it_returns_basic_fee(self, policy):
                    basic_fee = Fee(amount=2290, currency="KRW")
                    rate_discounted_fee = policy.apply_on(basic_fee)
                    expected = basic_fee - basic_fee * (PARKING_ZONE_ARTICLE["rate"] / 100)

                    assert_that(rate_discounted_fee).is_equal_to(expected)

