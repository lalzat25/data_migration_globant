from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from db import engine

Base=declarative_base()

class deparments(Base):
    __tablename__ = "deparments"
    id = Column(Integer, primary_key=True)
    deparment = Column(String)

Base.metadata.create_all(engine)