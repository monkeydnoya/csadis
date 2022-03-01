from fastapi import APIRouter, Depends
from . import models
from .schemas import AccessType
from dbsession import get_session
from sqlalchemy.orm import Session

accesstype_router = APIRouter(prefix='/access-type', tags=['access-type'])


@accesstype_router.get('/')
def get_access_type(db: Session = Depends(get_session)):
    access_types = db.query(models.AccessType).all()

    return access_types


@accesstype_router.post('/create', response_model=AccessType)
def create_access_type(access_type: AccessType, db: Session = Depends(get_session)):
    access_type_to_create = models.AccessType(**access_type.dict())

    db.add(access_type_to_create)
    db.commit()

    return access_type_to_create


@accesstype_router.put('/update/{access_type_id}',response_model=AccessType)
def update_access_type(access_type_id: int,access_type: AccessType , db: Session = Depends(get_session)):
    update_to_access_type = db.query(models.AccessType).filter(models.AccessType.id == access_type_id).first()
    update_to_access_type.type = access_type.type
    update_to_access_type.description = access_type.description

    db.commit()

    return update_to_access_type


@accesstype_router.delete('/delete/{access_type_id}',response_model=AccessType)
def delete_access_type(access_type_id: int, db: Session = Depends(get_session)):
    access_type_to_delete = db.query(models.AccessType).filter(models.AccessType.id == access_type_id).first()

    db.delete(access_type_to_delete)

    return access_type_to_delete