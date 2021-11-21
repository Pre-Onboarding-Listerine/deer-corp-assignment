from fastapi import APIRouter, Depends
from starlette import status

from src.dependencies import get_session_factory
from src.rate_policies.application.services import FeeCalculatorClient
from src.rate_policies.application.unit_of_work import SqlCalculatorUnitOfWork
from src.rate_policies.domain.models import Fee
from src.rate_policies.dto import RequestUsage

router = APIRouter(
    prefix="/policies"
)


@router.post("", status_code=status.HTTP_200_OK, response_model=Fee)
def calculate_fee(
        req_usage: RequestUsage,
        session_factory=Depends(get_session_factory)
):
    calculator_client = FeeCalculatorClient(uow=SqlCalculatorUnitOfWork(session_factory))
    return calculator_client.get_fee(user_id=req_usage.user_id, req_usage=req_usage)
