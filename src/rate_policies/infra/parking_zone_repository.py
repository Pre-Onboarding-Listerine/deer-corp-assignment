import abc
import json
from typing import List, Dict

from geoalchemy2 import functions
from geojson_pydantic import Feature, Point
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.rate_policies.domain.models import areas
from src.rate_policies.domain.models.areas import ParkingZone, Location
from src.rate_policies.infra import orm


class AbstractParkingZoneRepository(abc.ABC):
    @abc.abstractmethod
    def locate_in(self, area: areas.Area) -> List[ParkingZone]:
        raise NotImplementedError


class SqlParkingZoneRepository(AbstractParkingZoneRepository):
    def __init__(self, session: Session):
        self.session = session

    def locate_in(self, area: areas.Area) -> List[ParkingZone]:
        boundary = area.boundary_geom()
        zones = self.session.query(functions.ST_AsGeoJSON(orm.ParkingZone))\
            .filter(func.ST_Within(orm.ParkingZone.parkingzone_center, boundary)).all()
        ParkingZoneFeatureModel = Feature[Point, Dict]
        models = [ParkingZoneFeatureModel(**json.loads(zone[0])) for zone in zones]
        return [
            ParkingZone(
                parkingzone_id=model.properties["parkingzone_id"],
                parkingzone_center=Location(
                    lat=model.geometry.coordinates[0],
                    lng=model.geometry.coordinates[1]
                ),
                parkingzone_radius=model.properties["parkingzone_radius"]
            ) for model in models
        ]
