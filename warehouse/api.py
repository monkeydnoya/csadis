from fastapi import APIRouter, Depends
from . import models
from .schemas import WareHouse
from dbsession import get_session
from sqlalchemy.orm import Session


wh_router = APIRouter(prefix='/warehouse', tags=['warehouse'])


@wh_router.get('/')
def get_warehouse(db: Session = Depends(get_session)):
    warehouse = db.query(models.WareHouse).all()

    return warehouse


@wh_router.post('/create', response_model=WareHouse)
def create_warehouse(warehouse:WareHouse, db: Session = Depends(get_session)):
    warehouse_create = models.WareHouse(**warehouse.dict())

    db.add(warehouse_create)
    db.commit()

    return warehouse_create


@wh_router.put('/update/{warehouse_id}', response_model=WareHouse)
def update_warehouse(warehouse_id:int, warehouse:WareHouse, db: Session = Depends(get_session)):
    update_to_warehouse = db.query(models.WareHouse).filter(models.WareHouse.id==warehouse_id).first()
    update_to_warehouse.number = warehouse.number
    update_to_warehouse.address = warehouse.address

    db.commit()

    return update_to_warehouse


@wh_router.delete('/delete/{warehouse_id}',response_model=WareHouse)
def delete_warehouse(warehouse_id:int, db: Session = Depends(get_session)):
    warehouse_to_delete = db.query(models.WareHouse).filter(models.WareHouse.id == warehouse_id).first()

    db.delete(warehouse_to_delete)

    return warehouse_to_delete
