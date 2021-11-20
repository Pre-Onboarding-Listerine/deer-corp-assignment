from datetime import datetime, timedelta

import pytest
from assertpy import assert_that

from src.configs.discount_options import REUSE_STATEMENT
from src.rate_policies.domain.models import DeerUsage, UsageTime, Deer
from src.rate_policies.domain.models.areas import Location
from src.rate_policies.domain.models.statements import ReuseStatement
from tests.unit.fixtures.unit_of_work import FakeUsageRepository


class TestReuseStatement:
    @pytest.fixture
    def reuse_options(self):
        return REUSE_STATEMENT

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
    def last_usage(self, last_location, last_usage_time):
        return DeerUsage(
            user_id=1,
            use_deer=Deer(deer_name="deer-1", deer_area_id=1),
            end_location=last_location,
            usage_time=last_usage_time
        )

    @pytest.fixture
    def usage_repository(self, last_usage):
        return FakeUsageRepository({
            1: last_usage
        })

    @pytest.fixture
    def reuse_statement(self):
        return ReuseStatement

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
            def usage(self, end_location, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name="deer-1", deer_area_id=1),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, reuse_options, usage_repository):
                return ReuseStatement(
                    discount_amount=790,
                    options=reuse_options,
                    usages=usage_repository
                )

            def test_it_returns_true(self, statement, usage):
                actual = statement.is_applicable(usage)
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
            def usage(self, end_location, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name="deer-1", deer_area_id=1),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, reuse_options, usage_repository):
                return ReuseStatement(
                    discount_amount=790,
                    options=reuse_options,
                    usages=usage_repository
                )

            def test_it_returns_false(self, statement, usage):
                actual = statement.is_applicable(usage)
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
            def usage(self, end_location, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name="deer-2", deer_area_id=1),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, reuse_options, usage_repository):
                return ReuseStatement(
                    discount_amount=790,
                    options=reuse_options,
                    usages=usage_repository
                )

            def test_it_returns_false(self, statement, usage):
                actual = statement.is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)
