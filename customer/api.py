from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from . import models
from employee.models import Employee
from .schemas import Customer
from dbsession import get_session
from sqlalchemy.orm import Session
from log_config import get_logger
from check import *

import customer

customer_logger = get_logger(__name__)
customer_router = APIRouter(prefix='/customer', tags=['customer'])


@customer_router.get('/')
def get_customer(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'
    current_user = check_authorization_token(customer_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        customers = db.query(models.Customer).all()

        customer_logger.info(f"{method} request to localhost:8000/customer was executed successfully. Request was made by {current_user}")

    else:
        insufficient_access_level(customer_logger, method)

    return customers


@customer_router.get('/{customer_id}')
def get_customer_by_id(customer_id: int, Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = f'GET BY ID {customer_id}'
    current_user = check_authorization_token(customer_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        customers = db.query(models.Customer).filter(models.Customer.id==customer_id).first()

        customer_logger.info(f"{method} request to localhost:8000/customer/{customer_id} was executed successfully. Request was made by {current_user}")

    else:
        insufficient_access_level(customer_logger, method)
    
    return customers


@customer_router.post('/create', response_model=Customer)
def create_customer(customer:Customer,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'POST'
    current_user = check_authorization_token(customer_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 1 or current_user_access.post == 3:
        customer_create = models.Customer(**customer.dict())

        db.add(customer_create)
        db.commit()

        customer_logger.info(f"{method} request to localhost:8000/customer/create was executed successfully. Request was made by {current_user}")
    
    else:
        insufficient_access_level(customer_logger, method)

    return customer_create


@customer_router.put('/update/{customer_id}', response_model=Customer)
def update_customert(customer_id:int, customer:Customer,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'PUT'
    current_user = check_authorization_token(customer_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 1 or current_user_access.post == 3:    
        update_to_customer = db.query(models.Customer).filter(models.Customer.id==customer_id).first()
        update_to_customer.name = customer.name
        update_to_customer.address = customer.address

        db.commit()

        customer_logger.info(f"{method} request to localhost:8000/customer/update/{customer_id} was executed successfully. Request was made by {current_user}")
    
    else:
        insufficient_access_level(customer_logger, method)

    return update_to_customer


@customer_router.delete('/delete/{customer_id}',response_model=Customer)
def delete_customer(customer_id:int,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'DELETE'
    current_user = check_authorization_token(customer_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        customer_to_delete = db.query(models.Customer).filter(models.Customer.id == customer_id).first()

        db.delete(customer_to_delete)
        customer_logger.info(f"{method} request to localhost:8000/customer/delete/{customer_id} was executed successfully. Request was made by {current_user}")
    
    else:
        insufficient_access_level(customer_logger, method)

    return customer_to_delete
