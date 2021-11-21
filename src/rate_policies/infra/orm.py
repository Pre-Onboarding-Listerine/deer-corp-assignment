from geoalchemy2 import Geometry, Geography
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import composite, relationship

from src.configs.database import Base
from src.rate_policies.domain.models import Location


class Area(Base):
    __tablename__ = "areas"

    area_id = Column(Integer, primary_key=True, autoincrement=True)
    area_boundary = Column(Geometry(geometry_type='POLYGON'))
    area_lat = Column(Float)
    area_lng = Column(Float)

    area_center = composite(Location, area_lat, area_lng)


class ParkingZone(Base):
    __tablename__ = "parking_zones"

    parkingzone_id = Column(Integer, primary_key=True, autoincrement=True)
    parkingzone_center = Column(Geometry(geometry_type='POINT'))
    parkingzone_radius = Column(Float)


class ForbiddenArea(Base):
    __tablename__ = "forbidden_areas"

    forbidden_area_id = Column(Integer, primary_key=True, autoincrement=True)
    forbidden_area_boundary = Column(Geometry(geometry_type='POLYGON'))


class Deer(Base):
    __tablename__ = "deers"

    deer_name = Column(Integer, primary_key=True, autoincrement=True)
    deer_area_id = Column(Integer, ForeignKey('areas.area_id'))

    deer_area = relationship("Area")


class Usage(Base):
    __tablename__ = "usages"

    usage_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    use_deer_name = Column(Integer, ForeignKey('deers.deer_name'))
    use_end = Column(Geometry(geometry_type='POINT'))
    use_start_at = Column(DateTime)
    use_end_at = Column(DateTime)

    use_deer = relationship("Deer", uselist=True)
