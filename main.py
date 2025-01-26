from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import FastAPI, UploadFile, HTTPException, Depends
from db import get_db
from sql import dql

from models import departments, jobs, hired_employees
from services.validations import process_csv

app = FastAPI()

@app.post("/departments_list")
async def upload_departments(file:UploadFile,  session: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="File must be a CSV")
    num_records = await process_csv(file, departments.Departments, session=session)
    return {"message": f"{num_records} departments added successfully"}


@app.post("/job_list")
async def upload_jobs(file:UploadFile,  session: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="File must be a CSV")
    num_records = await process_csv(file, jobs.Jobs, session=session)
    return {"message": f"{num_records} jobs added successfully"}


@app.post("/hired_employes_list")
async def upload_jobs(file:UploadFile,  session: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="File must be a CSV")
    num_records = await process_csv(file, hired_employees.HiredEmployees, session=session)
    return {"message": f"{num_records} jobs added successfully"}

@app.get("/metrics/employees_by_quarter/")
async def employees_by_quarter(session: Session = Depends(get_db)):
    query = text(dql.queries["hired_employees_summary"])
    result = session.execute(query).fetchall()
    response = [
        {
            "department": row[0],
            "job": row[1],
            "Q1": row[2],
            "Q2": row[3],
            "Q3": row[4],
            "Q4": row[5],
        }
        for row in result
    ]

    return response

@app.get("/metrics/hired_by_deparment/")
async def hired_by_department(session: Session = Depends(get_db)):
    query = text(dql.queries["hired_by_department"])
    result = session.execute(query).fetchall()
    response = [
        {
            "id": row[0],
            "department": row[1],
            "hired": row[2]
        }
        for row in result
    ]

    return response

@app.get("/")
def root():
    return "OK"