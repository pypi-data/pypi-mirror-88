import json
from abc import ABC
from array import array

import jsonpickle

from .db_type import DBType
from .utils import typecheck


class DBCollection(DBType, ABC):
    """
    Base class for all collection objects
    """

    db_type = "TEXT"

    @classmethod
    @typecheck
    def value_to_str(cls, val) -> str:
        return f"'{json.dumps(jsonpickle.encode(val))}'"


class DBDict(DBCollection):
    python_type = dict


class DBList(DBCollection):
    python_type = list


class DBSet(DBCollection):
    python_type = set


class DBTuple(DBCollection):
    python_type = tuple


class DBArray(DBCollection):
    python_type = array
