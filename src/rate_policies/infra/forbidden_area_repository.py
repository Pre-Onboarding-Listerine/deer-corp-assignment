import abc

from sqlalchemy.orm import Session


class AbstractForbiddenAreaRepository(abc.ABC):
    pass


class SqlForbiddenAreaRepository(AbstractForbiddenAreaRepository):
    def __init__(self, session: Session
                 ):
        self.session = session
