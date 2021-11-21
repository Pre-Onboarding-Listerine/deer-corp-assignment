import abc

from geoalchemy2.shape import to_shape
from geojson_pydantic import Polygon
from sqlalchemy.orm import Session

from src.rate_policies.domain.models import Deer, areas
from src.rate_policies.exceptions import DeerNotFoundException
from src.rate_policies.infra import orm


class AbstractDeerRepository(abc.ABC):
    @abc.abstractmethod
    def get_deer_by_name(self, deer_name: int) -> Deer:
        raise NotImplementedError


class SqlDeerRepository(AbstractDeerRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_model(self, orm_deer: orm.Deer) -> Deer:
        boundary = to_shape(orm_deer.deer_area.area_boundary)
        coords = [list(map(lambda coord: list(coord), boundary.exterior.coords))]
        area_boundary = Polygon(coordinates=coords)

        deer_area = areas.Area(
            area_id=orm_deer.deer_area_id,
            area_boundary=area_boundary,
            area_center=orm_deer.deer_area.area_center
        )
        return Deer(deer_name=orm_deer.deer_name, deer_area=deer_area)

    def get_deer_by_name(self, deer_name: int) -> Deer:
        orm_deer = self.session.query(orm.Deer).filter(orm.Deer.deer_name == deer_name).first()
        if not orm_deer:
            raise DeerNotFoundException(f"deer {deer_name} is not found")
        return self._to_model(orm_deer)
