import contextlib

from sqlalchemy import Engine
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DatabaseManager:
    def __init__(self, dsn_string: str):
        self.engine: Engine = create_engine(url=dsn_string)
        self.sessionmaker = sessionmaker(bind=self.engine)

    def close(self):
        self.engine.dispose()

    @contextlib.contextmanager
    def session(self):
        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextlib.contextmanager
    def connect(self):
        with self.engine.connect() as connection:
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise
