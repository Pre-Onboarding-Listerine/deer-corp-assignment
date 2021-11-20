from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/policies"
)


@router.post("", status_code=status.HTTP_200_OK)
def calculate_fee(
        user_id: int
):
    pass
