from fastapi import APIRouter, Depends
from . import models
from schemas import Reserve
from sqlalchemy.orm import Session
from main import get_session


reserve_router = APIRouter(prefix='/reserve')


@reserve_router.get('/')
def get_reserve(db: Session = Depends(get_session)):
    reserve = 