from fastapi import FastAPI

from src.configs.database import Base, engine
from src.rate_policies.exception_handlers import different_currency_exception_handler, \
    different_type_operation_exception_handler, area_not_found_exception_handler, fee_not_found_exception_handler, \
    deer_not_found_exception_handler
from src.rate_policies.exceptions import DifferentCurrencyException, DifferentTypeOperationException, \
    AreaNotFoundException, FeeNotFoundException, DeerNotFoundException
from src.users.routers import router as user_router
from src.rate_policies.routers import router as policy_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(policy_router)

app.add_exception_handler(DifferentCurrencyException, different_currency_exception_handler)
app.add_exception_handler(DifferentTypeOperationException, different_type_operation_exception_handler)
app.add_exception_handler(AreaNotFoundException, area_not_found_exception_handler)
app.add_exception_handler(FeeNotFoundException, fee_not_found_exception_handler)
app.add_exception_handler(DeerNotFoundException, deer_not_found_exception_handler)
