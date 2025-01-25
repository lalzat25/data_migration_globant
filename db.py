from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

url=URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    host="localhost",
    database="postgres",
    port=5432
)


engine = create_engine(url)
Session=sessionmaker(bind=engine)
#session=Session()

def get_db() -> Session:
    db = Session()  # Create a new session
    try:
        yield db  # This will be the session passed to your route
    finally:
        db.close()