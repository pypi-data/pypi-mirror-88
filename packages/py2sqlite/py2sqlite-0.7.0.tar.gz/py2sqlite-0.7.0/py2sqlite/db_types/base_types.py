from abc import ABC

from .db_type import DBType
from .utils import typecheck


class DBBaseType(DBType, ABC):
    """
    Base class for all objects of basic types
    """

    @classmethod
    @typecheck
    def value_to_str(cls, val) -> str:
        return str(val)


class DBFloat(DBBaseType, ABC):
    db_type = "REAL"
    python_type = float


class DBInteger(DBBaseType, ABC):
    db_type = "INTEGER"
    python_type = int


class DBString(DBBaseType, ABC):
    db_type = "TEXT"
    python_type = str

    @classmethod
    @typecheck
    def value_to_str(cls, val) -> str:
        return "'" + str(val) + "'"
