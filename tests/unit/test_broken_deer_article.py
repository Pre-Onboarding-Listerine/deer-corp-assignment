from datetime import datetime

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon

from settings import except_options
from src.rate_policies.domain.models import areas, Location, UsageTime, DeerUsage, Deer, Fee
from src.rate_policies.domain.models.articles import BrokenDeerArticle


class TestBrokenDeerArticle:
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
    def exceptions_options(self):
        return except_options

    class TestWhenExitInLimit:
        @pytest.fixture
        def end_location(self):
            return Location(
                lat=37.541983,
                lng=127.078179
            )

        @pytest.fixture
        def usage_time(self):
            return UsageTime(
                start=datetime(2021, 11, 18, 8, 50, 0),
                end=datetime(2021, 11, 18, 8, 50, 30)
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
        def article(self, exceptions_options):
            return BrokenDeerArticle(options=exceptions_options["broken_deer"])

        class TestIsApplicable:
            def test_it_returns_true(self, article, usage):
                actual = article._is_applicable(usage)
                expected = True

                assert_that(actual).is_equal_to(expected)

        class TestCalculate:
            def test_it_returns_zero_fee(self, article, usage):
                calculated_fee = Fee(amount=8000, currency="KRW")
                actual = article.calculate(calculated_fee, usage)
                expected = Fee(amount=0, currency="KRW")
                assert_that(actual).is_equal_to(expected)

    class TestWhenExitAfterLimit:
        @pytest.fixture
        def end_location(self):
            return Location(
                lat=37.544061,
                lng=127.081604
            )

        @pytest.fixture
        def usage_time(self):
            return UsageTime(
                start=datetime(2021, 11, 18, 8, 50, 0),
                end=datetime(2021, 11, 18, 8, 52, 0)
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
        def article(self, exceptions_options):
            return BrokenDeerArticle(options=exceptions_options["broken_deer"])

        class TestIsApplicable:
            def test_it_returns_false(self, article, usage):
                actual = article._is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)

        class TestCalculate:
            class TestCalculate:
                def test_it_returns_calculated_fee(self, article, usage):
                    calculated_fee = Fee(amount=8000, currency="KRW")
                    actual = article.calculate(calculated_fee, usage)
                    assert_that(actual).is_equal_to(calculated_fee)
