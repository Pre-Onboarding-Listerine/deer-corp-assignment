from typing import List

from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import DeerUsage, areas
from src.rate_policies.domain.models.areas import ParkingZone, Location
from src.rate_policies.infra.area_repository import AbstractAreaRepository
from src.rate_policies.infra.deer_repository import AbstractDeerRepository
from src.rate_policies.infra.forbidden_area_repository import AbstractForbiddenAreaRepository
from src.rate_policies.infra.parking_zone_repository import AbstractParkingZoneRepository
from src.rate_policies.infra.usage_repository import AbstractUsageRepository


class FakeAreaRepository(AbstractAreaRepository):
    def __init__(self, areas):
        self._areas = areas

    def get_by_id(self, area_id: int) -> areas.Area:
        return self._areas[area_id]


class FakeDeerRepository(AbstractDeerRepository):
    def __init__(self, deers):
        self._deers = deers


class FakeUsageRepository(AbstractUsageRepository):
    def __init__(self, usages):
        self._usages = usages

    def get_right_before_usage(self, user_id: int) -> DeerUsage:
        return self._usages[user_id]


class FakeParkingZoneRepository(AbstractParkingZoneRepository):
    def __init__(self, parking_zones):
        self._parking_zones = parking_zones

    def locate_in(self, area: areas.Area) -> List[ParkingZone]:
        return self._parking_zones[area.area_id]


class FakeForbiddenAreaRepository(AbstractForbiddenAreaRepository):
    def __init__(self, forbidden_areas):
        self._forbidden_areas = forbidden_areas


class FakeCalculatorUnitOfWork(AbstractCalculatorUnitOfWork):
    def __init__(self):
        self.areas = FakeAreaRepository(dict())
        self.deers = FakeDeerRepository(dict())
        self.usages = FakeUsageRepository(dict())
        self.parking_zones = FakeParkingZoneRepository(dict())
        self.forbidden_areas = FakeForbiddenAreaRepository(dict())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
