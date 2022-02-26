from typing import Counter
import models
from fastapi import Depends, FastAPI
from schemas import Employee, CounterAgent
from database import SessionLocal
from sqlalchemy.orm import Session
from employee.api import employee_router


app = FastAPI()

# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.