import abc
import json
from typing import Dict

from geoalchemy2 import functions
from geojson_pydantic import Feature, Polygon
from sqlalchemy.orm import Session

from src.rate_policies.domain.models import areas, Location
from src.rate_policies.exceptions import AreaNotFoundException
from src.rate_policies.infra import orm


class AbstractAreaRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, area_id: int) -> areas.Area:
        raise NotImplementedError


class SqlAreaRepository(AbstractAreaRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, area_id: int) -> areas.Area:
        area = self.session.query(functions.ST_AsGeoJSON(orm.Area)).filter(orm.Area.area_id == area_id).first()
        if not area:
            raise AreaNotFoundException(f"area {area_id} is not found")
        area = json.loads(area[0])
        AreaFeatureModel = Feature[Polygon, Dict]
        area_model = AreaFeatureModel(**area)
        return areas.Area(
            area_id=area_model.properties["area_id"],
            area_boundary=area_model.geometry,
            area_center=Location(
                lat=area_model.properties["area_lat"],
                lng=area_model.properties["area_lng"]
            )
        )
