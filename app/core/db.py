from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine, MetaData
from app.core.config import settings, logger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

__all__ = ["get_db", "db_dependency", "Base", "engine", "display_metadata"]

kwargs = {}

if 'sqlite' in settings.SQLALCHEMY_DATABASE_URL:
    kwargs = {'connect_args': {'check_same_thread': False}}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, **kwargs)
metadata = MetaData()
metadata.reflect(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def display_metadata(meta_data: metadata = metadata):
    class DisplayCols:
        COLUMN = "-----Column-----"
        TYPE = "-----Type-----"
        PRIMARY_KEY = "---Primary Key---"
        NULLABLE = "---Nullable---"
        DEFAULT = "--Default--"
        FOREIGN_KEY = "---Foreign Key---"

        def __init__(self):
            self._col = self.COLUMN, len(self.COLUMN)
            self._type = self.TYPE, len(self.TYPE)
            self._pk = self.PRIMARY_KEY, len(self.PRIMARY_KEY)
            self._nul = self.NULLABLE, len(self.NULLABLE)
            self._def = self.DEFAULT, len(self.DEFAULT)
            self._fk = self.FOREIGN_KEY, len(self.FOREIGN_KEY)

        @property
        def heading(self) -> str:
            return f"+{self._col[0]}+{self._type[0]}+{self._pk[0]}+{self._nul[0]}+{self._def[0]}+{self._fk[0]}+"

        @property
        def footer(self) -> str:
            return f"+{'-'*self._col[1]}+{'-'*self._type[1]}+{'-'*self._pk[1]}+{'-'*self._nul[1]}+{'-'*self._def[1]}+{'-'*self._fk[1]}+"

        def print_column(self, column):
            _name = str(column.name)
            _type = str(column.type)
            _pk = str(column.primary_key)
            _nul = str(column.nullable)
            _def = str(column.default)
            _fk = ", ".join([column.table.name + "." + fk.column.name for fk in column.foreign_keys]) or "None"
            return f"|{_name:^{self._col[1]}}|{_type:^{self._type[1]}}|{_pk:^{self._pk[1]}}|{_nul:^{self._nul[1]}}|{_def:^{self._def[1]}}|{_fk:^{self._fk[1]}}|"

    ds = DisplayCols()

    logger.debug("Fetching Database Tables . . ")
    for table_name, table in meta_data.tables.items():
        logger.debug(f"Table : {str(table_name):=^20}")
        logger.debug(ds.heading)
        for column in table.columns:
            logger.debug(ds.print_column(column))
        logger.debug(ds.footer)


class ModelMixing(object):
    def __init__(self, session: Session):
        self.db = session

    def insert(self, data: object):
        pass

    def add_to_db(self, data: object):
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)

    def find_by_name(self, model: object, name: str) -> object | dict:
        response = self.db.query(model).filter_by(name=name).first()
        return response if response else {}
