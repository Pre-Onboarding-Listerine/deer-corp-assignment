import abc

from sqlalchemy.orm import Session

from src.rate_policies.domain.models import AreaFee, Fee
from src.rate_policies.exceptions import FeeNotFoundException
from src.rate_policies.infra import orm


class AbstractAreaFeeRepository(abc.ABC):
    @abc.abstractmethod
    def get_fee_of(self, area_id: int) -> AreaFee:
        raise NotImplementedError


class SqlAreaFeeRepository(AbstractAreaFeeRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_fee_of(self, area_id: int) -> AreaFee:
        area_fee = self.session.query(orm.AreaFee).filter(orm.AreaFee.area_id == area_id).first()
        if not area_fee:
            raise FeeNotFoundException(f"area fee of area {area_id} is not found")
        return AreaFee(
            area_id=area_id,
            base=Fee(amount=area_fee.base, currency=area_fee.currency),
            rate_per_minute=Fee(amount=area_fee.rate_per_minute, currency=area_fee.currency)
        )

