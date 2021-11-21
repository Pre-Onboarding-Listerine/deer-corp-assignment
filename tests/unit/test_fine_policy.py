from datetime import datetime

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon

from src.configs.discount_options import OUT_OF_RETURN_AREA_ARTICLE, FORBIDDEN_RETURN_AREA_ARTICLE
from src.rate_policies.domain.models import Fee, DeerUsage, UsageTime, AreaFee, Deer, areas
from src.rate_policies.domain.models.areas import Location
from src.rate_policies.domain.models.policies import FinePolicy
from tests.unit.fixtures.unit_of_work import FakeCalculatorUnitOfWork, FakeForbiddenAreaRepository, FakeAreaRepository


class TestFinePolicy:
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
    def out_of_forbidden_area(self):
        return Location(lat=37.537496, lng=127.068930)

    @pytest.fixture
    def in_forbidden_area(self):
        return Location(lat=37.455691, lng=127.1351404)

    @pytest.fixture
    def calculator_uow(self, deer_area, out_of_forbidden_area, in_forbidden_area):
        uow = FakeCalculatorUnitOfWork()
        uow.forbidden_areas = FakeForbiddenAreaRepository({
            out_of_forbidden_area.lat: False,
            in_forbidden_area.lat: True
        })
        uow.areas = FakeAreaRepository({
            1: deer_area
        })
        return uow

    @pytest.fixture
    def fine_policy(self):
        return FinePolicy

    class TestCalculate:

        class TestWhenReturnInForbiddenAreaAndOutOfArea:
            @pytest.fixture
            def end_location(self, in_forbidden_area):
                return in_forbidden_area

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
                def policy(self, fine_policy, usage, area_fee, calculator_uow):
                    options = {
                        "out_of_return_area": OUT_OF_RETURN_AREA_ARTICLE,
                        "forbidden_return_area": FORBIDDEN_RETURN_AREA_ARTICLE
                    }
                    return fine_policy(usage, area_fee, calculator_uow, options)

                def test_it_returns_basic_fee(self, policy, usage):
                    discounted_fee = Fee(amount=8000, currency="KRW")

                    fined_fee = policy.apply_on(discounted_fee)
                    expected = discounted_fee
                    for article in policy.articles:
                        expected = article.calculate(expected, usage)

                    assert_that(fined_fee).is_equal_to(expected)

