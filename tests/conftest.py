
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.configs.database import Base


pytest_plugins = [
    
]

TEST_SQLITE_URL = "sqlite:///:memory:"


@pytest.fixture
def in_memory_db():
    engine = create_engine(TEST_SQLITE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)
    Base.metadata.drop_all(bind=in_memory_db)
