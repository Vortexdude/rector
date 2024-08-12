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

        def __init__(self):
            self._col = self.COLUMN, len(self.COLUMN)
            self._type = self.TYPE, len(self.TYPE)
            self._pk = self.PRIMARY_KEY, len(self.PRIMARY_KEY)
            self._nul = self.NULLABLE, len(self.NULLABLE)
            self._def = self.DEFAULT, len(self.DEFAULT)

        @property
        def heading(self) -> str:
            return f"+{self._col[0]}+{self._type[0]}+{self._pk[0]}+{self._nul[0]}+{self._def[0]}+"

        @property
        def footer(self) -> str:
            return f"+{'-'*self._col[1]}+{'-'*self._type[1]}+{'-'*self._pk[1]}+{'-'*self._nul[1]}+{'-'*self._def[1]}+"

    _col = "-----Column-----"
    _type = "-----Type-----"
    _pk = '---Primary Key---'
    _nul = "---Nullable---"
    _def = "--Default--"
    logger.debug("Fetching Database Tables . . ")
    for table_name, table in meta_data.tables.items():
        logger.debug(f"Table : {str(table_name):=^20}")
        logger.debug(f"+{_col}+{_type}+{_pk}+{_nul}+{_def}+")
        for column in table.columns:
            logger.debug(f"|{str(column.name):^{len(_col)}}|{str(column.type):^14}|{str(column.primary_key): ^17}"
                         f"|{str(column.nullable): ^14}|{str(column.default): ^11}|")
        logger.debug(f"+{'-'*len(_col)}+{'-'*len(_type)}+{'-'*len(_pk)}+{'-'*len(_nul)}+{'-'*len(_def)}+")


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
