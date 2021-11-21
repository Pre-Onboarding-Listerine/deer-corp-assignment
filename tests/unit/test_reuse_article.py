from datetime import datetime, timedelta

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon

from src.configs.discount_options import REUSE_ARTICLE
from src.rate_policies.domain.models import DeerUsage, UsageTime, Deer, areas
from src.rate_policies.domain.models.areas import Location
from src.rate_policies.domain.models.articles import ReuseArticle
from tests.unit.fixtures.unit_of_work import FakeUsageRepository


class TestReuseArticle:
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
    def reuse_options(self):
        return REUSE_ARTICLE

    @pytest.fixture
    def last_location(self):
        return Location(
            lat=37.541983,
            lng=127.078179
        )

    @pytest.fixture
    def last_usage_time(self):
        return UsageTime(
            start=datetime(2021, 11, 18, 8, 20, 0),
            end=datetime(2021, 11, 18, 8, 50, 0)
        )

    @pytest.fixture
    def last_usage(self, deer_area, last_location, last_usage_time):
        return DeerUsage(
            user_id=1,
            use_deer=Deer(deer_name=1, deer_area=deer_area),
            end_location=last_location,
            usage_time=last_usage_time
        )

    @pytest.fixture
    def usage_repository(self, last_usage):
        return FakeUsageRepository({
            1: last_usage
        })

    @pytest.fixture
    def reuse_article(self):
        return ReuseArticle

    class TestIsApplicable:

        class TestWhenReuseInLimit:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.541983,
                    lng=127.078179
                )

            @pytest.fixture
            def usage_time(self, reuse_options):
                return UsageTime(
                    start=datetime(2021, 11, 18, 8, 50, 0) + timedelta(minutes=reuse_options["minutes"] - 10),
                    end=datetime(2021, 11, 18, 12, 10, 0)
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
            def article(self, reuse_options, usage_repository):
                return ReuseArticle(
                    discount_amount=790,
                    options=reuse_options,
                    usages=usage_repository
                )

            def test_it_returns_true(self, article, usage):
                actual = article._is_applicable(usage)
                expected = True

                assert_that(actual).is_equal_to(expected)

        class TestWhenReuseAfterLimit:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.544061,
                    lng=127.081604
                )

            @pytest.fixture
            def usage_time(self, reuse_options):
                return UsageTime(
                    start=datetime(2021, 11, 18, 8, 50, 0) + timedelta(minutes=reuse_options["minutes"] + 10),
                    end=datetime(2021, 11, 18, 12, 10, 0)
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
            def article(self, reuse_options, usage_repository):
                return ReuseArticle(
                    discount_amount=790,
                    options=reuse_options,
                    usages=usage_repository
                )

            def test_it_returns_false(self, article, usage):
                actual = article._is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)

        class TestWhenUseOtherDeer:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.544061,
                    lng=127.081604
                )

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
                    use_deer=Deer(deer_name=2, deer_area=deer_area),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def article(self, reuse_options, usage_repository):
                return ReuseArticle(
                    discount_amount=790,
                    options=reuse_options,
                    usages=usage_repository
                )

            def test_it_returns_false(self, article, usage):
                actual = article._is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)
