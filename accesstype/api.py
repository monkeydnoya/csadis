from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from . import models
from employee.models import Employee
from .schemas import AccessType
from dbsession import get_session
from sqlalchemy.orm import Session
from log_config import get_logger
from check import *

access_logger = get_logger(__name__)
accesstype_router = APIRouter(prefix='/access-type', tags=['access-type'])

# Для уровния доступа 2 возможность управления доступами

@accesstype_router.get('/')
def get_access_type(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'
    current_user = check_authorization_token(access_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post >= 2:
        access_types = db.query(models.AccessType).all()
        access_logger.info(f"{method} request to localhost:8000/access-type was executed successfully. Request was made by {current_user}")
    
    else:
        insufficient_access_level(access_logger, method)

    return access_types


@accesstype_router.post('/create', response_model=AccessType)
def create_access_type(access_type: AccessType,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'POST'

    current_user = check_authorization_token(access_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post >= 2:
        access_type_to_create = models.AccessType(**access_type.dict())

        db.add(access_type_to_create)
        db.commit()

        access_logger.info(f"{method} request to localhost:8000/access-type/create was executed successfully. Request was made by {current_user}")

    else:
        insufficient_access_level(access_logger, method)

    return access_type_to_create


@accesstype_router.put('/update/{access_type_id}',response_model=AccessType)
def update_access_type(access_type_id: int,access_type: AccessType,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'PUT'

    current_user = check_authorization_token(access_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post >= 2:
        update_to_access_type = db.query(models.AccessType).filter(models.AccessType.id == access_type_id).first()
        update_to_access_type.type = access_type.type
        update_to_access_type.description = access_type.description

        db.commit()

        access_logger.info(f"{method} request to localhost:8000/access-type//update/{access_type_id} was executed successfully. Request was made by {current_user}")

    else:
        insufficient_access_level(access_logger, method)

    return update_to_access_type


@accesstype_router.delete('/delete/{access_type_id}',response_model=AccessType)
def delete_access_type(access_type_id: int,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'DELETE'

    current_user = check_authorization_token(access_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post >= 2:
        access_type_to_delete = db.query(models.AccessType).filter(models.AccessType.id == access_type_id).first()

        db.delete(access_type_to_delete)

        access_logger.info(f"{method} request to localhost:8000/access-type//delete/{access_type_id} was executed successfully. Request was made by {current_user}")

    else:
        insufficient_access_level(access_logger, method)

    return access_type_to_delete