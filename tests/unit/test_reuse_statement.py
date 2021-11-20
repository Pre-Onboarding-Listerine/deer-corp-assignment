from datetime import datetime, timedelta

import pytest
from assertpy import assert_that

from src.configs.discount_options import REUSE_STATEMENT
from src.rate_policies.domain.models import Usage, UsageTime, Location
from src.rate_policies.domain.models.statements import ReuseStatement


class TestReuseStatement:
    @pytest.fixture
    def limit_minutes(self):
        return REUSE_STATEMENT["minutes"]

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
        return Usage(
            user_id=1,
            use_deer_name="deer-1",
            end_location=last_location,
            usage_time=last_usage_time
        )

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
            def usage_time(self, limit_minutes):
                return UsageTime(
                    start=datetime(2021, 11, 18, 8, 50, 0) + timedelta(minutes=limit_minutes - 10),
                    end=datetime(2021, 11, 18, 12, 10, 0)
                )

            @pytest.fixture
            def usage(self, end_location, usage_time):
                return Usage(
                    user_id=1,
                    use_deer_name="deer-1",
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, limit_minutes, last_usage):
                return ReuseStatement(limit=limit_minutes, last_usage=last_usage)

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
            def usage_time(self, limit_minutes):
                return UsageTime(
                    start=datetime(2021, 11, 18, 8, 50, 0) + timedelta(minutes=limit_minutes + 10),
                    end=datetime(2021, 11, 18, 12, 10, 0)
                )

            @pytest.fixture
            def usage(self, end_location, usage_time):
                return Usage(
                    user_id=1,
                    use_deer_name="deer-1",
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, limit_minutes, last_usage):
                return ReuseStatement(limit=limit_minutes, last_usage=last_usage)

            def test_it_returns_false(self, statement, usage):
                actual = statement.is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)

        class TestWhenUseOtherKickBoard:
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
                return Usage(
                    user_id=1,
                    use_deer_name="deer-2",
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, limit_minutes, last_usage):
                return ReuseStatement(limit=limit_minutes, last_usage=last_usage)

            def test_it_returns_false(self, statement, usage):
                actual = statement.is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)
