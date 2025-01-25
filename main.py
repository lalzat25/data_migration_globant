from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, UploadFile, HTTPException, Depends
from db import get_db

from models import deparments, jobs, hired_employees
from services.validations import process_csv

app = FastAPI()
@app.post("/deparments")
async def create_deparments(id:int, deparment:str, session: Session = Depends(get_db)):
    deparment = deparments(id=id,deparment=deparment)
    session.add(deparment)
    session.commit()
    return "deparment added"

@app.post("/departments_list")
async def upload_deparments(file:UploadFile,  session: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="File must be a CSV")
    num_records = process_csv(file, deparments, session=session)
    return {"message": f"{num_records} deparemnts added successfully"}

@app.post("/jobs")
async def create_jobs(id:int, job:str, session: Session = Depends(get_db)):
    job=jobs(id=id, job=job)
    session.add(job)
    session.commit()
    return "job added"

@app.post("/job_list")
async def upload_jobs(file:UploadFile,  session: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="File must be a CSV")
    num_records = process_csv(file, jobs, session=session)
    return {"message": f"{num_records} jobs added successfully"}

@app.post("/hired_employes")
async def create_hired_employees(id:int, name:str, datetime:datetime, deparment_id:str, job_id:str,  session: Session = Depends(get_db)):
    hired_employee=hired_employees(id=id, name=name, datetime=datetime, deparment_id=deparment_id, job_id=job_id)
    session.add(hired_employee)
    session.commit()
    return "hired employee added"

@app.post("/hired_employes_list")
async def upload_jobs(file:UploadFile,  session: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="File must be a CSV")
    num_records = process_csv(file, hired_employees, session=session)
    return {"message": f"{num_records} jobs added successfully"}


@app.get("/")
def root():
    return "OK"