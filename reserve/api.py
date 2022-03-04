from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from . import models
from employee.models import Employee
from .schemas import Reserve
from sqlalchemy.orm import Session
from dbsession import get_session
from log_config import get_logger
from check import *


reserve_logger = get_logger(__name__)
reserve_router = APIRouter(prefix='/reserve', tags=['reserve'])


@reserve_router.get('/')
def get_reserve(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'
    current_user = check_authorization_token(reserve_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post >= 0:
        reserve = db.query(models.Reserve).all()
        reserve_logger.info(f"{method} request to localhost:8000/reserve was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(reserve_logger, method)

    return reserve


@reserve_router.get('/{reserve_id}')
def get_reserve_by_id(reserve_id: int, Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = f'GET BY ID {reserve_id}'
    current_user = check_authorization_token(reserve_logger, Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email == current_user).first()

    if current_user_access.post >= 0:
        reserve = db.query(models.Reserve).filter(models.Reserve.id == reserve_id).first()
        reserve_logger.info(f"{method} request to localhost:8000/reserve/{reserve_id} was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(reserve_logger, method)

    return reserve


@reserve_router.post('/create', response_model=Reserve)
def create_reserve(reserve:Reserve,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'POST'
    current_user = check_authorization_token(reserve_logger, Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email == current_user).first()

    if current_user_access.post == 3:
        reserve_to_create = models.Reserve(**reserve.dict())

        db.add(reserve_to_create)
        db.commit()
        reserve_logger.info(f"{method} request to localhost:8000/reserve/create was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(reserve_logger, method)

    return reserve_to_create


@reserve_router.put('/update/{reserve_id}', response_model=Reserve)
def update_reserve(reserve_id: int, reserve:Reserve,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'PUT'
    current_user = check_authorization_token(reserve_logger, Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email == current_user).first()

    if current_user_access.post == 3:
        reserve_to_update = db.query(models.Reserve).filter(models.Reserve.id==reserve.id).first()
        reserve_to_update.id = reserve.id
        reserve_to_update.item = reserve.item
        reserve_to_update.warehouse = reserve.warehouse
        reserve_to_update.count = reserve.count

        db.commit()
        reserve_logger.info(f"{method} request to localhost:8000/reserve/update/{reserve_id} was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(reserve_logger, method)

    return reserve_to_update


@reserve_router.delete('/delete/{reserve_id}', response_model=Reserve)
def delete_reserve(reserve_id:int, reserve:Reserve,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'DELETE'
    current_user = check_authorization_token(reserve_logger, Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email == current_user).first()

    if current_user_access.post == 3:
        reserve_to_delete = db.query(models.Reserve).filter(models.Reserve.id==reserve.id).first()

        db.delete(reserve_to_delete)
        reserve_logger.info(f"{method} request to localhost:8000/reserve/delete/{reserve_id} was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(reserve_logger, method)

    return reserve_to_delete