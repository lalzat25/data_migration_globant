from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv('.env.cloud')

url = URL.create(
    drivername=os.getenv("DB_DRIVER"),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    port=int(os.getenv("DB_PORT", 5432))
)

engine = create_engine(url)
Session=sessionmaker(bind=engine)

def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()