from datetime import datetime

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon

from src.configs.discount_options import FORBIDDEN_RETURN_AREA_ARTICLE
from src.rate_policies.domain.models import DeerUsage, UsageTime, Deer, areas, Fee
from src.rate_policies.domain.models.areas import Location
from src.rate_policies.domain.models.articles import ForbiddenReturnAreaArticle
from tests.unit.fixtures.unit_of_work import FakeForbiddenAreaRepository


class TestForbiddenReturnAreaArticle:
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
        return Location(lat=37.539197, lng=127.067932)

    @pytest.fixture
    def forbidden_area_repository(self, out_of_forbidden_area, in_forbidden_area):
        return FakeForbiddenAreaRepository({
            out_of_forbidden_area.lat: False,
            in_forbidden_area.lat: True
        })

    @pytest.fixture
    def forbidden_return_area_article(self):
        return ForbiddenReturnAreaArticle

    class TestIsApplicable:

        class TestWhenReturnedForbiddenArea:
            @pytest.fixture
            def usage_time(self):
                return UsageTime(
                    start=datetime(2021, 11, 18, 9, 0, 0),
                    end=datetime(2021, 11, 18, 9, 10, 0)
                )

            @pytest.fixture
            def usage(self, deer_area, in_forbidden_area, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name=1, deer_area=deer_area),
                    end_location=in_forbidden_area,
                    usage_time=usage_time
                )

            @pytest.fixture
            def article(self, usage, forbidden_area_repository):
                return ForbiddenReturnAreaArticle(
                    fine_amount=FORBIDDEN_RETURN_AREA_ARTICLE["amount"],
                    options=FORBIDDEN_RETURN_AREA_ARTICLE,
                    forbidden_areas=forbidden_area_repository
                )

            def test_it_returns_true(self, article, usage):
                actual = article._is_applicable(usage)
                expected = True

                assert_that(actual).is_equal_to(expected)

        class TestWhenReturnedInProperArea:
            @pytest.fixture
            def usage_time(self):
                return UsageTime(
                    start=datetime(2021, 11, 18, 9, 0, 0),
                    end=datetime(2021, 11, 18, 9, 10, 0)
                )

            @pytest.fixture
            def usage(self, deer_area, out_of_forbidden_area, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name=1, deer_area=deer_area),
                    end_location=out_of_forbidden_area,
                    usage_time=usage_time
                )

            @pytest.fixture
            def article(self, usage, forbidden_area_repository):
                return ForbiddenReturnAreaArticle(
                    fine_amount=FORBIDDEN_RETURN_AREA_ARTICLE["amount"],
                    options=FORBIDDEN_RETURN_AREA_ARTICLE,
                    forbidden_areas=forbidden_area_repository
                )

            def test_it_returns_false(self, article, usage):
                actual = article._is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)

    class TestCalculate:

        class TestWhenReturnedForbiddenArea:
            @pytest.fixture
            def usage_time(self):
                return UsageTime(
                    start=datetime(2021, 11, 18, 9, 0, 0),
                    end=datetime(2021, 11, 18, 9, 10, 0)
                )

            @pytest.fixture
            def usage(self, deer_area, in_forbidden_area, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name=1, deer_area=deer_area),
                    end_location=in_forbidden_area,
                    usage_time=usage_time
                )

            @pytest.fixture
            def article(self, usage, forbidden_area_repository):
                return ForbiddenReturnAreaArticle(
                    fine_amount=FORBIDDEN_RETURN_AREA_ARTICLE["amount"],
                    options=FORBIDDEN_RETURN_AREA_ARTICLE,
                    forbidden_areas=forbidden_area_repository
                )

            def test_it_returns_fined_fee(self, article, usage):
                discounted_fee = Fee(amount=8000, currency="KRW")
                fined_fee = article.calculate(discounted_fee, usage)
                expected = discounted_fee + Fee(amount=FORBIDDEN_RETURN_AREA_ARTICLE["amount"], currency="KRW")
                assert_that(fined_fee).is_equal_to(expected)

        class TestWhenReturnedInProperArea:
            @pytest.fixture
            def usage_time(self):
                return UsageTime(
                    start=datetime(2021, 11, 18, 9, 0, 0),
                    end=datetime(2021, 11, 18, 9, 10, 0)
                )

            @pytest.fixture
            def usage(self, deer_area, out_of_forbidden_area, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name=1, deer_area=deer_area),
                    end_location=out_of_forbidden_area,
                    usage_time=usage_time
                )

            @pytest.fixture
            def article(self, usage, forbidden_area_repository):
                return ForbiddenReturnAreaArticle(
                    fine_amount=FORBIDDEN_RETURN_AREA_ARTICLE["amount"],
                    options=FORBIDDEN_RETURN_AREA_ARTICLE,
                    forbidden_areas=forbidden_area_repository
                )

            def test_it_returns_non_increased_fee(self, article, usage):
                discounted_fee = Fee(amount=8000, currency="KRW")
                fined_fee = article.calculate(discounted_fee, usage)
                assert_that(fined_fee).is_equal_to(discounted_fee)
