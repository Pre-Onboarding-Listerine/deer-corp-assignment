import abc

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.rate_policies.domain.models import Location
from src.rate_policies.infra import orm


class AbstractForbiddenAreaRepository(abc.ABC):
    @abc.abstractmethod
    def includes(self, returned_location: Location) -> bool:
        raise NotImplementedError


class SqlForbiddenAreaRepository(AbstractForbiddenAreaRepository):
    def __init__(self, session: Session):
        self.session = session

    def includes(self, returned_location: Location) -> bool:
        exists = self.session.query(orm.ForbiddenArea).filter(
            func.ST_Contains(
                orm.ForbiddenArea.forbidden_area_boundary, returned_location.to_point()
            )).scalar()
        if exists:
            return True
        else:
            return False
