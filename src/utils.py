import os
import shutil
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _load_env(env_name: str) -> str:
    env_value = os.environ.get(env_name)

    if not env_value:
        raise Exception(f'{env_name} environment variable is not set')

    return env_value


def _get_db_connection():
    db_conn_string = _load_env('DB_CONN_STRING')

    engine = create_engine(db_conn_string)

    s = sessionmaker(bind=engine)

    return s(), engine


@contextmanager
def db_session_context():
    s, eng = _get_db_connection()
    try:
        yield s, eng
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


def move_file(file_name: str):
    shutil.move(f'data/{file_name}', f'processed_data/{file_name}')


def get_file_names(dir: str):
    return os.listdir(dir)
