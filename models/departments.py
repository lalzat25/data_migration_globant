from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from db import engine

Base=declarative_base()

class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    department = Column(String)

Base.metadata.create_all(engine)