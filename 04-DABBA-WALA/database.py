from sqlmodel import SQLModel, create_engine, Session

# database layer for fast api 
DATABASE_URL = "sqlite:///dabbawala.db"


engine = create_engine(DATABASE_URL, echo=True)

#create table for our DB  
def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """Provides a new database session.
    """
    with Session(engine) as session:
        yield session