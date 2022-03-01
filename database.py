from click import echo
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:hiraishin@localhost/csadis"

engine = create_engine(DATABASE_URL, echo = True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


