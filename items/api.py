from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from . import models
from employee.models import Employee
from .schemas import Items
from sqlalchemy.orm import Session
from dbsession import get_session
from log_config import get_logger
from check import *

items_logger = get_logger(__name__)
items_router = APIRouter(prefix='/items', tags=['items'])


@items_router.get('/')
def get_items(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'
    current_user = check_authorization_token(items_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        items = db.query(models.Items).all()
        items_logger.info(f"{method} request to localhost:8000/items was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(items_logger, method)

    return items


@items_router.get('/{item_id}')
def get_items_by_id(item_id: int,Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'
    current_user = check_authorization_token(items_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        items = db.query(models.Items).filter(models.Items.id == item_id).first()
        items_logger.info(f"{method} request to localhost:8000/items/{item_id} was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(items_logger, method)

    return items

@items_router.post('/create', response_model=Items)
def create_items(items: Items,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'POST'
    current_user = check_authorization_token(items_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 1 or current_user_access.post == 3:
        items_to_create = models.Items(**items.dict())

        db.add(items_to_create)
        db.commit()
        items_logger.info(f"{method} request to localhost:8000/items/create was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(items_logger, method)

    return items_to_create


@items_router.put('/update/{item_id}', response_model=Items)
def update_items(item_id: int, items: Items,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'PUT'
    current_user = check_authorization_token(items_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 1 or current_user_access.post == 3:
        items_to_update = db.query(models.Items).filter(models.Items.id==item_id).first()
        items_to_update.name = items.name
        items_to_update.type = items.type
        items_to_update.price = items.price
        items_to_update.currency = items.currency

        db.commit()
        items_logger.info(f"{method} request to localhost:8000/items/update/{item_id} was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(items_logger, method)
    return items_to_update


@items_router.delete('/delete/{item_id}',response_model=Items)
def delete_item(item_id: int, items: Items,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'DELETE'
    current_user = check_authorization_token(items_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 1 or current_user_access.post == 3:
        item_to_delete = db.query(models.Items).filter(models.Items.id==items.id).firs()

        db.delete(item_to_delete)
        items_logger.info(f"{method} request to localhost:8000/items/delete/{item_id} was executed successfully. Request was made by {current_user}")
    else:
        insufficient_access_level(items_logger, method)
        
    return item_to_delete