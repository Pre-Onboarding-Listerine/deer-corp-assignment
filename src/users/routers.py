from fastapi import APIRouter

router = APIRouter(
    prefix="/users"
)


@router.get("/hello")
def user_hello():
    return "user_hello"
