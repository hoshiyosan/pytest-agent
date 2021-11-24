from concurrent.futures import ProcessPoolExecutor

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pytest_agent.database import DBModel
from pytest_agent.settings import MAX_WORKER_PROCESSES, SQLALCHEMY_DATABASE_URL

executor = ProcessPoolExecutor(MAX_WORKER_PROCESSES)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
DBModel.metadata.create_all(engine)
session = scoped_session(session_factory=sessionmaker(bind=engine))
