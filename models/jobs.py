from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from db import engine

Base=declarative_base()

class Jobs(Base):
    __tablename__="jobs"
    id=Column(Integer, primary_key=True)
    job=Column(String)

Base.metadata.create_all(engine)