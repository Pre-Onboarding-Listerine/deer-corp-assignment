from sqlalchemy import Column, String, Integer

from src.configs.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)
