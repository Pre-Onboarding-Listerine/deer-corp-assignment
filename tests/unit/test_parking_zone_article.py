from datetime import datetime

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon

from src.configs.discount_options import PARKING_ZONE_ARTICLE
from src.rate_policies.domain.models import DeerUsage, UsageTime, Deer, areas
from src.rate_policies.domain.models.areas import Location, ParkingZone
from src.rate_policies.domain.models.articles import ParkingZoneArticle
from tests.unit.fixtures.unit_of_work import FakeParkingZoneRepository


class TestParkingZoneArticle:
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
    def parking_zone_article(self):
        return ParkingZoneArticle

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
            def usage(self, deer_area, end_location, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name=1, deer_area=deer_area),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def article(self, usage, parking_zone_repository):
                return ParkingZoneArticle(
                    discount_rate=PARKING_ZONE_ARTICLE["rate"],
                    parking_zones=parking_zone_repository
                )

            def test_it_returns_true(self, article, usage):
                actual = article._is_applicable(usage)
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
            def usage(self, deer_area, end_location, usage_time):
                return DeerUsage(
                    user_id=1,
                    use_deer=Deer(deer_name=1, deer_area=deer_area),
                    end_location=end_location,
                    usage_time=usage_time
                )

            @pytest.fixture
            def article(self, usage, parking_zone_repository):
                return ParkingZoneArticle(
                    discount_rate=PARKING_ZONE_ARTICLE["rate"],
                    parking_zones=parking_zone_repository
                )

            def test_it_returns_false(self, article, usage):
                actual = article._is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)
