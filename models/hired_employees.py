from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from db import engine

Base=declarative_base()

class HiredEmployees(Base):
    __tablename__="hired_employees"
    id=Column(Integer, primary_key=True)
    name=Column(String)
    datetime=Column(DateTime)
    department_id=Column(Integer)
    job_id=Column(Integer)

Base.metadata.create_all(engine)