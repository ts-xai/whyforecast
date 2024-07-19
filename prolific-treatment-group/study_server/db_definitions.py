from dataclasses import dataclass
from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import Column, String, TIMESTAMP, JSON, Integer
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base


@dataclass
class DBConfiguration:
    debug: bool
    path: str


# "magic" to make sure SQLite3 enforces foreign key constraints and uses the efficient WAL journal mode
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, _connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.close()


def db_engine(db_config: DBConfiguration):
    target = f"sqlite:///{db_config.path}"
    engine = create_engine(target, echo=db_config.debug)
    Base.metadata.create_all(engine)
    return engine


# database naming convention is to use camelCase and singular nouns throughout

Base = declarative_base()


class Participant(Base):
    __tablename__ = "participant"

    id = Column(String, primary_key=True)
    prolific_id = Column("prolificid", String, nullable=False)
    start = Column(TIMESTAMP(timezone=True), nullable=False)  # filled in when user has given consent
    end = Column(TIMESTAMP(timezone=True), nullable=True)  # filled in when user completed the study
    extra = Column(JSON, nullable=True)  # extra values stored during the study
    survey = Column(JSON, nullable=True)  # survey responses after the study

class FormData(Base):
    __tablename__ = 'form_data'
    id = Column(String)
    prolific_id = Column("prolificid", String, primary_key=True, nullable=False)
    round_number = Column(Integer, primary_key=True, nullable=False)
    first_form_value = Column(String)
    second_form_value = Column(String)
