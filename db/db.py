from sqlmodel import create_engine, Session, SQLModel
from db.config import host, user, password
DB_URL = f"postgresql://{user}:{password}@{host}:5432/First_api"

engine = create_engine(DB_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_database():
    SQLModel.metadata.create_all(engine)