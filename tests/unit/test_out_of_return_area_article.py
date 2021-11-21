from datetime import datetime

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon
from geopy.distance import distance
from shapely import geometry

from src.configs.discount_options import OUT_OF_RETURN_AREA_ARTICLE
from src.rate_policies.domain.models import DeerUsage, UsageTime, Deer, areas, Fee
from src.rate_policies.domain.models.areas import Location
from src.rate_policies.domain.models.articles import OutOfReturnAreaArticle
from tests.unit.fixtures.unit_of_work import FakeAreaRepository


class TestOutOfReturnAreaArticle:
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
    def area_repository(self, deer_area):
        return FakeAreaRepository({
            1: deer_area
        })

    @pytest.fixture
    def out_of_return_area_article(self):
        return OutOfReturnAreaArticle

    class TestIsApplicable:

        class TestWhenReturnedOutOfArea:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.455691,
                    lng=127.1351404
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
            def article(self, usage, area_repository):
                return OutOfReturnAreaArticle(
                    fine_rate=OUT_OF_RETURN_AREA_ARTICLE["rate_per_meter"],
                    options=OUT_OF_RETURN_AREA_ARTICLE,
                    areas=area_repository
                )

            def test_it_returns_true(self, article, usage):
                actual = article._is_applicable(usage)
                expected = True

                assert_that(actual).is_equal_to(expected)

        class TestWhenReturnedInProperArea:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.542271,
                    lng=127.077395
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
            def article(self, usage, area_repository):
                return OutOfReturnAreaArticle(
                    fine_rate=OUT_OF_RETURN_AREA_ARTICLE["rate_per_meter"],
                    options=OUT_OF_RETURN_AREA_ARTICLE,
                    areas=area_repository
                )

            def test_it_returns_false(self, article, usage):
                actual = article._is_applicable(usage)
                expected = False

                assert_that(actual).is_equal_to(expected)

    class TestCalculate:

        class TestWhenReturnedOutOfArea:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.455691,
                    lng=127.1351404
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
            def article(self, usage, area_repository):
                return OutOfReturnAreaArticle(
                    fine_rate=OUT_OF_RETURN_AREA_ARTICLE["rate_per_meter"],
                    options=OUT_OF_RETURN_AREA_ARTICLE,
                    areas=area_repository
                )

            def test_it_returns_fee_in_proportion_to_over_distance(self, article, usage):
                discounted_fee = Fee(amount=8000, currency="KRW")
                area = article.areas.get_by_id(1)
                boundary = geometry.Polygon(*area.area_boundary.coordinates)
                line = geometry.LineString([area.area_center.tuple(), usage.end_location.tuple()])
                intersection_points = list(boundary.intersection(line).coords)
                min_distance = min(distance(intersection_points[0], usage.end_location.tuple()),
                                   distance(intersection_points[1], usage.end_location.tuple()))

                fined_fee = article.calculate(discounted_fee, usage)
                fine = Fee(amount=OUT_OF_RETURN_AREA_ARTICLE["rate_per_meter"], currency="KRW") * min_distance.m
                expected = discounted_fee + fine

                assert_that(fined_fee).is_equal_to(expected)

        class TestWhenReturnedInProperArea:
            @pytest.fixture
            def end_location(self):
                return Location(
                    lat=37.542271,
                    lng=127.077395
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
            def article(self, usage, area_repository):
                return OutOfReturnAreaArticle(
                    fine_rate=OUT_OF_RETURN_AREA_ARTICLE["rate_per_meter"],
                    options=OUT_OF_RETURN_AREA_ARTICLE,
                    areas=area_repository
                )

            def test_it_returns_non_increased_fee(self, article, usage):
                discounted_fee = Fee(amount=8000, currency="KRW")
                fined_fee = article.calculate(discounted_fee, usage)
                assert_that(fined_fee).is_equal_to(discounted_fee)
