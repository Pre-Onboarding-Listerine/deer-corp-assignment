from datetime import datetime

import pytest
from assertpy import assert_that
from geojson_pydantic import Polygon

from src.rate_policies.application.unit_of_work import SqlCalculatorUnitOfWork
from src.rate_policies.domain import models
from src.rate_policies.domain.models import areas, Location, AreaFee, Fee, Deer
from src.rate_policies.exceptions import AreaNotFoundException
from src.rate_policies.infra import orm


def orm_area():
    return orm.Area(area_boundary='POLYGON((37.543272 127.076550, 37.541734 127.074072, 37.539088 127.074490, 37.538928 127.078034, 37.540417 127.080781, 37.542416 127.080599, 37.543272 127.076550))', area_lat=37.541302, area_lng=127.077852)


def insert_areas(session):
    session.add(orm_area())


def test_get_area_with_exist_id(session_factory):
    session = session_factory()
    insert_areas(session)
    session.commit()

    uow = SqlCalculatorUnitOfWork(session_factory)
    with uow:
        area = uow.areas.get_by_id(area_id=1)
        assert_that(area).is_instance_of(areas.Area)
        assert_that(area.area_center).is_equal_to(Location(lat=37.541302, lng=127.077852))


def test_get_area_with_not_exist_id(session_factory):
    uow = SqlCalculatorUnitOfWork(session_factory)
    with uow:
        assert_that(uow.areas.get_by_id).raises(AreaNotFoundException).when_called_with(area_id=1)


@pytest.fixture
def model_area():
    return areas.Area(
        area_id=1,
        area_boundary=Polygon(coordinates=[[(37.543272, 127.07655), (37.541734, 127.074072), (37.539088, 127.07449), (37.538928, 127.078034), (37.540417, 127.080781), (37.542416, 127.080599), (37.543272, 127.07655)]], type='Polygon'),
        area_center=Location(lat=37.541302, lng=127.077852),
    )


def insert_usages(session):
    session.add(orm_area())

    session.add(orm.Deer(deer_area_id=1))

    session.add(orm.Usage(user_id=1, use_deer_name=1,
                          use_end=Location(lat=37.455691, lng=127.1351404).to_point(),
                          use_start_at=datetime(2021, 11, 18, 9, 0, 0), use_end_at=datetime(2021, 11, 18, 9, 10, 0)))
    session.add(orm.Usage(user_id=1, use_deer_name=1,
                          use_end=Location(lat=37.544061, lng=127.081604).to_point(),
                          use_start_at=datetime(2021, 11, 18, 8, 0, 0), use_end_at=datetime(2021, 11, 18, 8, 20, 0)))


def test_get_last_usage(session_factory):
    session = session_factory()
    insert_usages(session)
    session.commit()

    uow = SqlCalculatorUnitOfWork(session_factory)
    with uow:
        last_usage = uow.usages.get_right_before_usage(user_id=1)
        assert_that(last_usage).is_instance_of(models.DeerUsage)
        assert_that(last_usage.usage_time.end).is_equal_to(datetime(2021, 11, 18, 9, 10, 0))


def insert_parking_zones(session):
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.542169 127.078315)', parkingzone_radius=50))
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.541118 127.077741)', parkingzone_radius=50))
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.539974 127.079415)', parkingzone_radius=50))
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.535404 127.077021)', parkingzone_radius=50))


def test_get_parking_zones_in_polygon(session_factory, model_area):
    session = session_factory()
    insert_parking_zones(session)
    session.commit()

    uow = SqlCalculatorUnitOfWork(session_factory)
    with uow:
        parking_zones = uow.parking_zones.locate_in(model_area)
        assert_that(parking_zones[0]).is_instance_of(areas.ParkingZone)
        assert_that(len(parking_zones)).is_equal_to(3)


def insert_forbidden_area(session):
    session.add(orm.ForbiddenArea(forbidden_area_boundary='POLYGON((37.540201 127.067682, 37.538789 127.066912, 37.538108 127.068822, 37.539588 127.069487, 37.540201 127.067682))'))
    session.add(orm.ForbiddenArea(forbidden_area_boundary='POLYGON((37.537630 127.066173, 37.537034 127.065911, 37.536404 127.067842, 37.537004 127.068099, 37.537630 127.066173))'))
    session.add(orm.ForbiddenArea(forbidden_area_boundary='POLYGON((37.537420 127.069609, 37.536663 127.069251, 37.536433 127.069981, 37.537173 127.070378, 37.537420 127.069609))'))


def test_get_forbidden_area_contains_point(session_factory):
    session = session_factory()
    insert_forbidden_area(session)
    session.commit()

    uow = SqlCalculatorUnitOfWork(session_factory)
    with uow:
        out_of_forbidden_area = Location(lat=37.537496, lng=127.068930)
        is_included = uow.forbidden_areas.includes(out_of_forbidden_area)
        assert_that(is_included).is_equal_to(False)

        in_forbidden_area = Location(lat=37.539197, lng=127.067932)
        is_included = uow.forbidden_areas.includes(in_forbidden_area)
        assert_that(is_included).is_equal_to(True)


def insert_area_fees(session):
    session.add(orm_area())
    session.add(orm_area())

    session.add(orm.AreaFee(area_id=1, base=790, rate_per_minute=150, currency="KRW"))
    session.add(orm.AreaFee(area_id=2, base=300, rate_per_minute=70, currency="KRW"))


def test_get_area_fee_by_area_id(session_factory):
    session = session_factory()
    insert_area_fees(session)
    session.commit()

    uow = SqlCalculatorUnitOfWork(session_factory)
    with uow:
        kunk_area_fee = uow.area_fees.get_fee_of(area_id=1)
        assert_that(kunk_area_fee).is_instance_of(AreaFee)
        assert_that(kunk_area_fee.base).is_equal_to(Fee(amount=790, currency="KRW"))

        yeosu_area_fee = uow.area_fees.get_fee_of(area_id=2)
        assert_that(yeosu_area_fee.base).is_equal_to(Fee(amount=300, currency="KRW"))
        assert_that(yeosu_area_fee.rate_per_minute).is_equal_to(Fee(amount=70, currency="KRW"))


def insert_deer(session):
    session.add(orm_area())

    session.add(orm.Deer(deer_name=1, deer_area_id=1))


def test_get_deer_by_name(session_factory):
    session = session_factory()
    insert_deer(session)
    session.commit()

    uow = SqlCalculatorUnitOfWork(session_factory)
    with uow:
        deer = uow.deers.get_deer_by_name(deer_name=1)
        assert_that(deer).is_instance_of(Deer)
