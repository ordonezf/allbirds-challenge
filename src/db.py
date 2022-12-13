from typing import Dict, List, Any

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean

from utils import db_session_context


def create_table(base):
    with db_session_context() as (_, engine):
        base.metadata.create_all(engine)


def _create_db_class(table_specs: List[Dict], table_name: str) -> Any:
    """Dynamically generates a db class based on the table specs.
    It creates the table in the database if it doesn't exist.
    Returns the db class.

    Based on this article: http://sparrigan.github.io/sql/sqla/2016/01/03/dynamic-tables.html"""

    type_map = {'TEXT': String, 'INTEGER': Integer, 'BOOLEAN': Boolean}
    columns = {column['column name']: Column(type_map[column['datatype']]) for column in table_specs}
    columns['id'] = Column(Integer, primary_key=True, autoincrement=True)
    attr_dict = {'__tablename__': table_name, **columns}

    Base = declarative_base()
    cls = type(f'{table_name}Class', (Base,), attr_dict)

    create_table(Base)

    return cls


def create_db_objects(parsed_rows: List[Dict], table_specs: List[Dict], table_name: str) -> List[Any]:
    """Create db objects from parsed rows."""

    db_objects = []
    cls = _create_db_class(table_specs, table_name)
    for row in parsed_rows:
        attrs = {col['column_name']: col['column_value'] for col in row}
        db_objects.append(cls(**attrs))

    return db_objects


def insert_into_db(objects_to_insert: List[Any]):
    """Inserts objects into the database."""

    with db_session_context() as (session, _):
        for obj in objects_to_insert:
            session.add(obj)
