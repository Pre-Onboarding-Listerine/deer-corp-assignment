from sqlalchemy import Column, String

from src.configs.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)
