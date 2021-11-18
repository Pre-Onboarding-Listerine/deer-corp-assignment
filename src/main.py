from fastapi import FastAPI

from src.configs.database import Base, engine
from src.users.routers import router as user_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
