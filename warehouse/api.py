from fastapi import APIRouter, Depends,status
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from . import models
from employee.models import Employee
from .schemas import WareHouse
from dbsession import get_session
from sqlalchemy.orm import Session
from log_config import get_logger
from check import *

wh_logger = get_logger(__name__)
wh_router = APIRouter(prefix='/warehouse', tags=['warehouse'])


@wh_router.get('/')
def get_warehouse(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'

    current_user = check_authorization_token(wh_logger,Authorize)
    current_user_access = db.query(Employee).filter(Employee.email==current_user).first()

    if current_user_access.post >= 3:
        warehouse = db.query(models.WareHouse).all()
        wh_logger.info('GET request to localhost:8000/warehouse was executed successfully. Request was made by {current_user}')
    
    else:
        insufficient_access_level(wh_logger, method)

    return warehouse


@wh_router.get('/{wh_id}')
def get_warehouse(wh_id: int, Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = f'GET BU ID {wh_id}'

    current_user = check_authorization_token(wh_logger,Authorize)
    current_user_access = db.query(Employee).filter(Employee.email==current_user).first()

    if current_user_access.post >= 3:
        warehouse = db.query(models.WareHouse).filter(models.WareHouse.id == wh_id).first()
        wh_logger.info('GET request to localhost:8000/warehouse was executed successfully. Request was made by {current_user}')
    
    else:
        insufficient_access_level(wh_logger, method)

    return warehouse


@wh_router.post('/create', response_model=WareHouse)
def create_warehouse(warehouse:WareHouse,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'POST'

    current_user = check_authorization_token(wh_logger,Authorize)
    current_user_access = db.query(Employee).filter(Employee.email==current_user).first()

    if current_user_access.post >= 2:
        warehouse_create = models.WareHouse(**warehouse.dict())

        db.add(warehouse_create)
        db.commit()
        wh_logger.info('GET request to localhost:8000/warehouse/create was executed successfully. Request was made by {current_user}')

    else:
        insufficient_access_level(wh_logger, method)
    return warehouse_create


@wh_router.put('/update/{warehouse_id}', response_model=WareHouse)
def update_warehouse(warehouse_id:int, warehouse:WareHouse,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'PUT'
    current_user = check_authorization_token(wh_logger,Authorize)
    current_user_access = db.query(Employee).filter(Employee.email==current_user).first()

    if current_user_access.post >= 2:
        update_to_warehouse = db.query(models.WareHouse).filter(models.WareHouse.id==warehouse_id).first()
        update_to_warehouse.number = warehouse.number
        update_to_warehouse.address = warehouse.address

        db.commit()
        wh_logger.info('GET request to localhost:8000/warehouse/update/{warehouse_id} was executed successfully. Request was made by {current_user}')
    
    else:
        insufficient_access_level(wh_logger, method)

    return update_to_warehouse


@wh_router.delete('/delete/{warehouse_id}',response_model=WareHouse)
def delete_warehouse(warehouse_id:int,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'DELETE'

    current_user = check_authorization_token(wh_logger,Authorize)
    current_user_access = db.query(Employee).filter(Employee.email==current_user).first()

    if current_user_access >= 3:
        warehouse_to_delete = db.query(models.WareHouse).filter(models.WareHouse.id == warehouse_id).first()

        db.delete(warehouse_to_delete)
        wh_logger.info('GET request to localhost:8000/warehouse/delete/{warehouse_id} was executed successfully. Request was made by {current_user}')
    
    else:
        insufficient_access_level(wh_logger, method)

    return warehouse_to_delete
