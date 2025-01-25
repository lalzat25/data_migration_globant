import csv
from sqlalchemy.orm import Session
from io import StringIO
from fastapi import HTTPException

def process_csv(file, model, session: Session):
    content = file.read().decode("utf-8")
    csv_data = StringIO(content)
    csv_reader = csv.reader(csv_data)

    records = []

    for index, row in enumerate(csv_reader):
        if len(row) != len(model.__table__.columns):
            raise HTTPException(
                status_code=400,
                detail=f"Row {index +1} is invalid. Expected {expected_columns} columns, got {len(row)}"
            )
        try:
            record = model(**{model.__table__.columns.keys()[i]:row[i] for i in range(expected_columns)})
            records.append(record)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing row {index+1}: {str(e)}"
            )
        
    session.add_all(records)
    session.commit()
    return len(records)
