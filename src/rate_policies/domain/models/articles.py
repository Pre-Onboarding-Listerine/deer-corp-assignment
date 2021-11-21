import abc
from datetime import timedelta

from geopy.distance import distance
from shapely.geometry import Polygon, Point, LineString

from src.rate_policies.domain.models import DeerUsage, Fee
from src.rate_policies.exceptions import DifferentCurrencyException, DifferentTypeOperationException
from src.rate_policies.infra.area_repository import AbstractAreaRepository
from src.rate_policies.infra.forbidden_area_repository import AbstractForbiddenAreaRepository
from src.rate_policies.infra.parking_zone_repository import AbstractParkingZoneRepository
from src.rate_policies.infra.usage_repository import AbstractUsageRepository


class Article(abc.ABC):
    usage: DeerUsage

    @abc.abstractmethod
    def _is_applicable(self, usage: DeerUsage) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def calculate(self, fee: Fee, usage: DeerUsage) -> Fee:
        raise NotImplementedError


class ParkingZoneArticle(Article):
    def __init__(self, discount_rate: float, parking_zones: AbstractParkingZoneRepository):
        self.discount_rate = discount_rate
        self.parking_zones = parking_zones

    def _is_applicable(self, usage: DeerUsage) -> bool:
        available_zones = self.parking_zones.locate_in(usage.use_deer.deer_area)
        for zone in available_zones:
            if zone.includes(usage.end_location):
                return True
        return False

    def calculate(self, fee: Fee, usage: DeerUsage) -> Fee:
        if self._is_applicable(usage):
            try:
                return fee - fee * (self.discount_rate / 100)
            except DifferentCurrencyException:
                return fee
            except DifferentTypeOperationException:
                return fee
        else:
            return fee


class ReuseArticle(Article):
    def __init__(self, discount_amount: float, options: dict, usages: AbstractUsageRepository):
        self.discount_amount = discount_amount
        self.currency = options["currency"]
        self.limit = timedelta(minutes=options["minutes"])
        self.usages = usages

    def _is_applicable(self, usage: DeerUsage) -> bool:
        last_usage = self.usages.get_right_before_usage(user_id=usage.user_id)
        if last_usage.use_deer.deer_name != usage.use_deer.deer_name:
            return False
        reuse_delta = usage.usage_time.start - last_usage.usage_time.end
        if self.limit < reuse_delta:
            return False
        return True

    def calculate(self, fee: Fee, usage: DeerUsage) -> Fee:
        if self._is_applicable(usage):
            try:
                return fee - Fee(amount=self.discount_amount, currency=self.currency)
            except DifferentCurrencyException:
                return fee
            except DifferentTypeOperationException:
                return fee
        return fee


class OutOfReturnAreaArticle(Article):
    def __init__(self, fine_rate: float, options: dict, areas: AbstractAreaRepository):
        self.fine_rate = fine_rate
        self.currency = options["currency"]
        self.areas = areas
        self.deer_end_location = None

    def _is_applicable(self, usage: DeerUsage) -> bool:
        self.deer_end_location = usage.end_location
        boundary = Polygon(*usage.use_deer.deer_area.area_boundary.coordinates)
        if not boundary.contains(Point(self.deer_end_location.tuple())):
            return True
        else:
            return False

    def calculate(self, fee: Fee, usage: DeerUsage) -> Fee:
        if self._is_applicable(usage):
            boundary = Polygon(*usage.use_deer.deer_area.area_boundary.coordinates)
            line = LineString([usage.use_deer.deer_area.area_center.tuple(), self.deer_end_location.tuple()])
            intersection_points = list(boundary.intersection(line).coords)
            min_distance = min(distance(intersection_points[0], self.deer_end_location.tuple()),
                               distance(intersection_points[1], self.deer_end_location.tuple()))
            return fee + Fee(amount=self.fine_rate, currency=self.currency) * min_distance.m
        return fee


class ForbiddenReturnAreaArticle(Article):
    def __init__(self, fine_amount: float, options: dict, forbidden_areas: AbstractForbiddenAreaRepository):
        self.fine_amount = fine_amount
        self.currency = options["currency"]
        self.forbidden_areas = forbidden_areas

    def _is_applicable(self, usage: DeerUsage) -> bool:
        returned_location = usage.end_location
        if self.forbidden_areas.includes(returned_location):
            return True
        else:
            return False

    def calculate(self, fee: Fee, usage: DeerUsage) -> Fee:
        if self._is_applicable(usage):
            try:
                return fee + Fee(amount=self.fine_amount, currency=self.currency)
            except DifferentCurrencyException:
                return fee
            except DifferentTypeOperationException:
                return fee
        return fee
