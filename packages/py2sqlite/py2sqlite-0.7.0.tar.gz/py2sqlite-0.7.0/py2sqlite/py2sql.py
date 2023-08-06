import logging
import os
import sqlite3
from typing import List, Tuple, Any, Type

from py2sqlite.db_objects import DBObject, ForeignKey, Column
from .db_types import DBInteger
from .queries import insert_object_query, create_table_query, find_object_by_pk_query, update_object_by_pk_query, \
    modify_table_query, delete_object_query, delete_table_query


class Py2SQL:
    """
    Main class for handling all ORM operations
    """

    def __init__(self):
        self.__connection: sqlite3.Connection = None

    @property
    def cursor(self) -> sqlite3.dbapi2.Cursor:
        return self.__connection.cursor()

    def db_connect(self, db_name=":memory:") -> None:
        """
        Connect to the sqlite3 database

        :param db_name: db filename. If not set - create db in memory
        :return:
        """
        try:
            self.__connection = sqlite3.connect(db_name)
            cursor = self.cursor
            cursor.execute("""PRAGMA foreign_keys = ON""")
        except sqlite3.Error:
            logging.exception("Error connecting to database")

    def db_disconnect(self) -> None:
        """
        Disconnect from currently connected database
        """
        if self.__connection:
            self.__connection.close()
        else:
            logging.exception("Database was not connected")

    def db_engine(self) -> str:
        """
        Get db engine info

        :return: db engine name and version
        """
        return f"SQLite3 {sqlite3.sqlite_version}"

    def db_name(self, get_paths=False) -> List[str]:
        """
        Get list of current databases filenames or full paths

        :param get_paths: whether to return full paths instead of filenames
        :return:
        """
        curr_table = self.__run_single_query("PRAGMA database_list;")
        curr_table = [x[2] for x in curr_table]
        if not get_paths:
            curr_table = [os.path.basename(x) for x in curr_table]
        return curr_table

    def db_tables(self) -> List[str]:
        """
        Get tables available in the connected database

        :return: list of table names
        """
        return Py2SQL.__flatten_structure(self.__run_single_query("SELECT name FROM sqlite_master WHERE type='table';"))

    def db_size(self) -> int:
        """
        Get size of the connected database

        :return: size of database in Mb
        """
        page_count = self.__run_single_query_flatten("PRAGMA page_count;")[0]
        page_size = self.__run_single_query_flatten("PRAGMA page_size")[0]
        return page_size * page_count / (1024 * 1024)

    def db_table_structure(self, table: str) -> List[Tuple[int, str, str]]:
        """
        Get list of tuples with info about table attributes

        :return: list of tuples of ids, names and types
        """
        res = self.__run_single_query(f"PRAGMA table_info('{table}')")
        return [(int(x[0]), str(x[1]), str(x[2])) for x in res]

    def db_table_size(self, table: str):
        """
        Get estimated size of table

        :return: estimated size of table in Mb
        """
        return self.__run_single_query_flatten(f"""
            SELECT COUNT(*) *  -- The number of rows in the table
             ( 24 +        -- The length of all 4 byte int columns
               12 +        -- The length of all 8 byte int columns
               128 )       -- The estimate of the average length of all string columns
            FROM {table}
            """)[0] / (1024 * 1024)

    # py -> sql

    def save_object(self, db_object: DBObject):
        """
        Add object to database

        :param db_object: object to add
        """
        if not isinstance(db_object, DBObject):
            logging.warning(f"Can only save objects inherited from DBObject")
            return
        if db_object.hierarchy_ref():
            ref: Column = db_object.hierarchy_ref()

            values_to_save = {}
            par_cols: List[Column] = ref.col_type.class_columns()
            par_cols = [x for x in par_cols if not (x.col_type == DBInteger and x.primary_key)]

            for c in par_cols:
                values_to_save[c.name] = db_object.__getattribute__(c.name)

            ref_table: Type[DBObject] = ref.col_type
            ref_pk = ref_table.class_primary_keys()[0]
            setattr(db_object, f"hierarchy_ref_{ref.col_type.__name__}", ref_table(**values_to_save))

        # add all aggregated DBObjects recursively
        recursive = db_object.obj_columns()
        if db_object.hierarchy_ref():
            recursive.append(db_object.hierarchy_ref())
        for col in recursive:
            if issubclass(col.col_type, DBObject):
                self.save_object(getattr(db_object, col.name))

        p_k = db_object.obj_primary_keys()
        p_k = [x for x in p_k if x.col_type != DBInteger]
        if len(p_k) == 0 or len(self._find_by_pk(db_object)) == 0:
            q = insert_object_query(db_object)
            self.__run_single_query(q, commit=True)
        else:
            q = update_object_by_pk_query(db_object)
            self.__run_single_query(q, commit=True)

        # update autoincremented integer primary key value in object
        if db_object.pk_name is not None:
            pk = db_object.pk_name
            if getattr(db_object.__class__, pk).col_type == DBInteger:
                setattr(db_object, pk, self.max_id(db_object.__class__, pk))

    def _find_by_pk(self, db_object: DBObject):
        q = find_object_by_pk_query(db_object, False)
        return self.__run_single_query_flatten(q)

    def save_class(self, db_class: Type[DBObject]):
        """
        Add table to database

        :param db_class: class with a corresponding table to add
        """
        # add all aggregated DBObjects tables recursively
        for col in db_class.class_columns():
            if issubclass(col.col_type, DBObject):
                self.save_class(col.col_type)

        col_info = self.__run_single_query(f"PRAGMA table_info('{db_class.__table_name__}')")
        # print(col_info)
        if len(col_info) > 0:
            q = modify_table_query(db_class, col_info)
            # print(q)
            cursor = self.cursor
            cursor.executescript(q)
            self.__connection.commit()
        else:
            q = create_table_query(db_class)
            refs: List[Type[DBObject]] = []
            Py2SQL.__traverse_references(db_class, refs)

            for k in refs:
                self.save_class(k)

            self.__run_single_query(q, commit=True)

    @staticmethod
    def __traverse_references(root: Type[DBObject], res: List[Any]) -> List[Type[DBObject]]:
        fk: List[ForeignKey] = root.class_foreign_keys()
        for k in fk:
            ref = k.ref_table
            if ref not in res:
                res.append(ref)
                Py2SQL.__traverse_references(ref, res)
        return res

    def save_hierarchy(self, root_class: Type[DBObject]):
        """
        Add table of a root class along with tables of all its subclasses to database

        :param root_class: root class
        """
        self.save_class(root_class)
        subclasses = root_class.__subclasses__()
        for s in subclasses:
            self.save_hierarchy(s)

    def delete_object(self, db_object: DBObject):
        """
        Delete object from database

        :param db_object: object to delete
        """
        q = delete_object_query(db_object)
        self.__run_single_query(q, commit=True)

    def delete_class(self, db_class: Type[DBObject]):
        """
        Delete table from database

        :param db_class: class with corresponding table to delete
        """
        q = delete_table_query(db_class)
        self.__run_single_query(q, commit=True)

    def delete_hierarchy(self, root_class):
        """
        Delete table of a root class along with tables of all its subclasses from database

        :param root_class: root class
        """
        self.delete_class(root_class)
        subclasses = root_class.__subclasses__()
        for s in subclasses:
            self.delete_hierarchy(s)

    def max_id(self, table: Type[DBObject], column_name: str):
        """
        Find max column value in table

        :param table: table to be searched
        :param column_name: column name on which to search max value
        :return: max value
        """
        res = self.__run_single_query_flatten(f"""SELECT max({column_name}) FROM {table.__table_name__};""")[0]
        return res

    def __run_single_query(self, query, commit=False) -> List[Any]:
        cursor = self.cursor
        cursor.execute(query)
        res = cursor.fetchall()
        if commit:
            self.__connection.commit()
        return res

    def __run_single_query_flatten(self, query) -> List[Any]:
        return Py2SQL.__flatten_structure(self.__run_single_query(query))

    @staticmethod
    def __flatten_structure(structure) -> List[Any]:
        return [i for level in structure for i in level]
