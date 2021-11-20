import abc
from typing import List

from sqlalchemy.orm import Session

from src.rate_policies.domain.models.areas import ParkingZone


class AbstractParkingZoneRepository(abc.ABC):
    @abc.abstractmethod
    def locate_in(self, area_id: int) -> List[ParkingZone]:
        raise NotImplementedError


class SqlParkingZoneRepository(AbstractParkingZoneRepository):
    def __init__(self, session: Session):
        self.session = session

    def locate_in(self, area_id: int) -> List[ParkingZone]:
        pass
