"""
Utils to access database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = None


def create_db_engine(db_conn_string, debug_mode=False):
    return create_engine(db_conn_string,
                         echo=debug_mode,
                         pool_size=1,
                         max_overflow=0,
                         pool_recycle=3600,
                         pool_pre_ping=True,
                         pool_use_lifo=True)


def create_db_session(engine):
    global Session
    if not Session:
        Session = sessionmaker(bind=engine)
    return Session()