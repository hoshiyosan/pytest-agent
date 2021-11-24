from sqlalchemy import Column, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base

DBModel = declarative_base()


class DBTest(DBModel):
    __tablename__ = "tests"

    fullname = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    refresh_date = Column(Float, nullable=False)
    output = Column(Text, nullable=True)
