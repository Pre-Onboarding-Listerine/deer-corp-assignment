from datetime import datetime

from src.rate_policies.application.unit_of_work import AbstractCalculatorUnitOfWork
from src.rate_policies.domain.models import DeerUsage, Fee, Deer, UsageTime, Location
from src.rate_policies.domain.models.calculator import FeeCalculator
from src.rate_policies.dto import RequestUsage


class FeeCalculatorClient:
    def __init__(self, uow: AbstractCalculatorUnitOfWork):
        self.uow = uow

    def get_fee(self, user_id: int, req_usage: RequestUsage) -> Fee:
        with self.uow:
            use_deer = self.uow.deers.get_deer_by_name(deer_name=req_usage.use_deer_name)

            usage_time = UsageTime(
                start=datetime.strptime(req_usage.use_start_at, "%Y-%m-%d %H:%M:%S"),
                end=datetime.strptime(req_usage.use_end_at, "%Y-%m-%d %H:%M:%S")
            )

            end_location = Location(
                lat=req_usage.use_end_lat,
                lng=req_usage.use_ned_lng
            )

            usage = DeerUsage(
                user_id=user_id,
                use_deer=use_deer,
                end_location=end_location,
                usage_time=usage_time
            )

            calculator = FeeCalculator(uow=self.uow)
            return calculator.calculate_with(usage)
