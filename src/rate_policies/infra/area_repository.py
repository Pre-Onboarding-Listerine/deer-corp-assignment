import abc

from sqlalchemy.orm import Session


class AbstractAreaRepository(abc.ABC):
    pass


class SqlAreaRepository(AbstractAreaRepository):
    def __init__(self, session: Session):
        self.session = session
