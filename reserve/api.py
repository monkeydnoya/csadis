from fastapi import APIRouter, Depends
from . import models
from .schemas import Reserve
from sqlalchemy.orm import Session
from dbsession import get_session


reserve_router = APIRouter(prefix='/reserve')


@reserve_router.get('/')
def get_reserve(db: Session = Depends(get_session)):
    reserve = db.query(models.Reserve).all()

    return reserve


@reserve_router.post('/create', response_model=Reserve)
def create_reserve(reserve:Reserve, db: Session = Depends(get_session)):
    reserve_to_create = models.Reserve(**reserve.dict())

    db.add(reserve_to_create)
    db.commit()

    return reserve_to_create


@reserve_router.put('/update/{reserve_id}', response_model=Reserve)
def update_reserve(reserve_id: int, reserve:Reserve, db: Session = Depends(get_session)):
    reserve_to_update = db.query(models.Reserve).filter(models.Reserve.id==reserve.id).first()
    reserve_to_update.id = reserve.id
    reserve_to_update.item = reserve.item
    reserve_to_update.warehouse = reserve.warehouse
    reserve_to_update.count = reserve.count

    db.commit()

    return reserve_to_update


@reserve_router.delete('/delete/{reserve_id}', response_model=Reserve)
def delete_reserve(reserve_id:int, reserve:Reserve, db: Session = Depends(get_session)):
    reserve_to_delete = db.query(models.Reserve).filter(models.Reserve.id==reserve.id).first()

    db.delete(reserve_to_delete)


    return reserve_to_delete