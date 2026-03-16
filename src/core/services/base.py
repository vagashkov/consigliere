from typing import Any


class BaseService:
    """ Base class for all services """
    pass


class DBEnabledService(BaseService):
    """ Base class for all services that use a database """

    def __init__(self, session: Any):
        self.session = session
