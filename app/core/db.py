from typing import Optional
from sqlalchemy import create_engine, String, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

DATABASE_URL = "sqlite:///test.db"

Base = declarative_base()

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    nickname: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String(30))


def get_db():
    ins = inspect(engine)
    if not ins.has_table("users"):
        Base.metadata.create_all(bind=engine)
    database = session_local()
    try:
        yield database
    finally:
        database.close()
