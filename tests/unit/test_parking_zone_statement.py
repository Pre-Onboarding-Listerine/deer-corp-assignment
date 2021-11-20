from datetime import datetime

import pytest
from assertpy import assert_that

from src.configs.discount_options import PARKING_ZONE_STATEMENT
from src.rate_policies.domain.models import DeerUsage, UsageTime, Deer
from src.rate_policies.domain.models.areas import Location, ParkingZone
from src.rate_policies.domain.models.statements import ParkingZoneStatement
from tests.unit.fixtures.unit_of_work import FakeParkingZoneRepository


class TestParkingZoneStatement:
    @pytest.fixture
    def parking_zone_repository(self):
        return FakeParkingZoneRepository({
            1: [
                ParkingZone(
                    parkingzone_id=1,
                    parkingzone_center=Location(lat=37.541732, lng=127.079799),
                    parkingzone_radius=200
                )
            ]
        })

    @pytest.fixture
    def parking_zone_statement(self):
        return ParkingZoneStatement

    class TestIsApplicable:

        class TestWhenReturnedInParkingZone:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.541983,
                    lng=127.078179
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
                    use_deer=Deer(deer_name="deer-1", deer_area_id=1),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, usage, parking_zone_repository):
                return ParkingZoneStatement(
                    discount_rate=PARKING_ZONE_STATEMENT["rate"],
                    parking_zones=parking_zone_repository
                )

            def test_it_returns_true(self, statement, usage):
                actual = statement.is_applicable(usage)
                expected = True

                assert_that(actual).is_equal_to(expected)

        class TestWhenReturnedOutOfParkingZone:
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
                    use_deer=Deer(deer_name="deer-1", deer_area_id=1),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def statement(self, usage, parking_zone_repository):
                return ParkingZoneStatement(
                    discount_rate=PARKING_ZONE_STATEMENT["rate"],
                    parking_zones=parking_zone_repository
                )

            def test_it_returns_false(self, statement, usage):
                actual = statement.is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)
