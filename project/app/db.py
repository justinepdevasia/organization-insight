import os
from sqlmodel import create_engine,Session


DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
#engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
