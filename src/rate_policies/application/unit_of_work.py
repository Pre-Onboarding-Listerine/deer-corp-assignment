from __future__ import annotations
import abc

from src.rate_policies.infra.area_repository import AbstractAreaRepository, SqlAreaRepository
from src.rate_policies.infra.deer_repository import AbstractDeerRepository, SqlDeerRepository
from src.rate_policies.infra.forbidden_area_repository import AbstractForbiddenAreaRepository, \
    SqlForbiddenAreaRepository
from src.rate_policies.infra.parking_zone_repository import AbstractParkingZoneRepository, SqlParkingZoneRepository
from src.rate_policies.infra.usage_repository import AbstractUsageRepository, SqlUsageRepository


class AbstractCalculatorUnitOfWork(abc.ABC):
    areas: AbstractAreaRepository
    deers: AbstractDeerRepository
    forbidden_areas: AbstractForbiddenAreaRepository
    parking_zones: AbstractParkingZoneRepository
    usages: AbstractUsageRepository

    def __enter__(self) -> AbstractCalculatorUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlCalculatorUnitOfWork(AbstractCalculatorUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.areas = SqlAreaRepository(self.session)
        self.deers = SqlDeerRepository(self.session)
        self.forbidden_areas = SqlForbiddenAreaRepository(self.session)
        self.parking_zones = SqlParkingZoneRepository(self.session)
        self.usages = SqlUsageRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

