import abc
from geoalchemy2.shape import to_shape
from geojson_pydantic import Polygon
from sqlalchemy.orm import Session

from src.rate_policies.domain.models import DeerUsage, Deer, areas, Location, UsageTime
from src.rate_policies.infra import orm


class AbstractUsageRepository(abc.ABC):
    @abc.abstractmethod
    def get_right_before_usage(self, user_id: int) -> DeerUsage:
        raise NotImplementedError


class SqlUsageRepository(AbstractUsageRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_model(self, usage: orm.Usage) -> DeerUsage:
        end_location = to_shape(usage.use_end)
        boundary = to_shape(usage.use_deer[0].deer_area.area_boundary)
        coords = [list(map(lambda coord: list(coord), boundary.exterior.coords))]
        area_boundary = Polygon(coordinates=coords)

        deer_area = areas.Area(
            area_id=usage.use_deer[0].deer_area_id,
            area_boundary=area_boundary,
            area_center=usage.use_deer[0].deer_area.area_center
        )

        use_deer = Deer(
            deer_name=usage.use_deer_name,
            deer_area=deer_area
        )

        return DeerUsage(
            user_id=usage.user_id,
            use_deer=use_deer,
            end_location=Location(lat=end_location.x, lng=end_location.y),
            usage_time=UsageTime(start=usage.use_start_at, end=usage.use_end_at)
        )

    def get_right_before_usage(self, user_id: int) -> DeerUsage:
        usage = self.session.query(orm.Usage)\
            .filter(orm.Usage.user_id == user_id).order_by(orm.Usage.use_end_at.desc()).first()
        return self._to_model(usage)
