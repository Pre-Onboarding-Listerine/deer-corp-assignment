import abc

from sqlalchemy.orm import Session


class AbstractDeerRepository(abc.ABC):
    pass


class SqlDeerRepository(AbstractDeerRepository):
    def __init__(self, session: Session):
        self.session = session
