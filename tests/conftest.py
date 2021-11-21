import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.configs.database import Base
from src.rate_policies.infra.orm import Area
from src.rate_policies.infra.orm import ParkingZone
from src.rate_policies.infra.orm import ForbiddenArea
from src.rate_policies.infra.orm import Usage
from src.rate_policies.infra.orm import Deer


pytest_plugins = [
    "tests.unit.fixtures.unit_of_work",
]

# TEST_SQLITE_URL = "sqlite:///:memory:"
TEST_MYSQL_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


@pytest.fixture
def in_memory_db():
    engine = create_engine(TEST_MYSQL_URL, encoding='utf-8')
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)
    Base.metadata.drop_all(bind=in_memory_db)
