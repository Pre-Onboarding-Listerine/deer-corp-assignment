from datetime import datetime

from src.configs.database import SessionLocal
from src.rate_policies.domain.models import Location
from src.rate_policies.infra import orm


def insert_areas(session):
    session.add(orm.Area(area_boundary='POLYGON((37.543272 127.076550, 37.541734 127.074072, 37.539088 127.074490, 37.538928 127.078034, 37.540417 127.080781, 37.542416 127.080599, 37.543272 127.076550))', area_lat=37.541302, area_lng=127.077852))
    session.add(orm.Area(area_boundary='POLYGON((37.492470 127.119119, 37.490733 127.120288, 37.492087 127.122766, 37.493772 127.121339, 37.492470 127.119119))', area_lat=37.492291, area_lng=127.120824))


def insert_deers(session):
    session.add(orm.Deer(deer_name=1, deer_area_id=1))
    session.add(orm.Deer(deer_name=2, deer_area_id=2))


def insert_usages(session):
    session.add(orm.Usage(user_id=1, use_deer_name=1,
                          use_end=Location(lat=37.455691, lng=127.1351404).to_point(),
                          use_start_at=datetime(2021, 11, 18, 9, 0, 0), use_end_at=datetime(2021, 11, 18, 9, 10, 0)))
    session.add(orm.Usage(user_id=1, use_deer_name=1,
                          use_end=Location(lat=37.544061, lng=127.081604).to_point(),
                          use_start_at=datetime(2021, 11, 18, 8, 0, 0), use_end_at=datetime(2021, 11, 18, 8, 20, 0)))
    session.add(orm.Usage(user_id=2, use_deer_name=2,
                          use_end=Location(lat=37.492679, lng=127.121521).to_point(),
                          use_start_at=datetime(2021, 11, 18, 8, 0, 0), use_end_at=datetime(2021, 11, 18, 8, 20, 0)))


def insert_parking_zones(session):
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.542169 127.078315)', parkingzone_radius=50))
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.541118 127.077741)', parkingzone_radius=50))
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.539974 127.079415)', parkingzone_radius=50))
    session.add(orm.ParkingZone(parkingzone_center='POINT(37.535404 127.077021)', parkingzone_radius=50))


def insert_forbidden_area(session):
    session.add(orm.ForbiddenArea(forbidden_area_boundary='POLYGON((37.540201 127.067682, 37.538789 127.066912, 37.538108 127.068822, 37.539588 127.069487, 37.540201 127.067682))'))
    session.add(orm.ForbiddenArea(forbidden_area_boundary='POLYGON((37.537630 127.066173, 37.537034 127.065911, 37.536404 127.067842, 37.537004 127.068099, 37.537630 127.066173))'))
    session.add(orm.ForbiddenArea(forbidden_area_boundary='POLYGON((37.537420 127.069609, 37.536663 127.069251, 37.536433 127.069981, 37.537173 127.070378, 37.537420 127.069609))'))


def insert_area_fees(session):
    session.add(orm.AreaFee(area_id=1, base=790, rate_per_minute=150, currency="KRW"))
    session.add(orm.AreaFee(area_id=2, base=300, rate_per_minute=70, currency="KRW"))


def main():
    print("start db initializing")
    session = SessionLocal()
    insert_areas(session)
    insert_deers(session)
    insert_usages(session)
    insert_parking_zones(session)
    insert_forbidden_area(session)
    insert_area_fees(session)
    session.commit()
    print("complete db initializing")


if __name__ == "__main__":
    main()



