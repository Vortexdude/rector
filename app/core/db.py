from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from app.core.config import settings

__all__ = ["get_db", "db_dependency", "Base", "engine"]

kwargs = {}

if 'sqlite' in settings.SQLALCHEMY_DATABASE_URL:
    kwargs = {'connect_args': {'check_same_thread': False}}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, **kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


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
