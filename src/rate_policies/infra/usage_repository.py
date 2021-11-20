import abc

from sqlalchemy.orm import Session

from src.rate_policies.domain.models import DeerUsage


class AbstractUsageRepository(abc.ABC):
    @abc.abstractmethod
    def get_right_before_usage(self, user_id: int) -> DeerUsage:
        raise NotImplementedError


class SqlUsageRepository(AbstractUsageRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_right_before_usage(self, user_id: int) -> DeerUsage:
        pass
