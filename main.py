from fastapi import FastAPI
from db import session
from models.deparments import deparments

app = FastAPI()

@app.post("/")
async def create_deparments(id:int, deparment:str):
    deparment = deparments(id=id,deparment=deparment)
    session.add(deparment)
    session.commit()
    return "deparment added"

@app.get("/")
def root():
    return "OK"