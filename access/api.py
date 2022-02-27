from . import models
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import Access
from dbsession import get_session


access_router = APIRouter(prefix='/access', tags=['access'])


@access_router.get('/')
def get_access(db: Session = Depends(get_session)):
    access = db.query(models.Access).all()

    return access


@access_router.post('/create')
def create_access(access: Access, db: Session = Depends(get_session)):
    access_to_create = models.Access(**access.dict())

    db.add(access_to_create)
    db.commit()

    return access_to_create


@access_router.put('/update/{access_employee}')
def update_access(access_employee: str, access: Access, db: Session = Depends(get_session)):
    access_to_update = db.query(models.Access).filter(models.Access.employee==access_employee).first()
    access_to_update.employee = access.employee
    access_to_update.warehouse = access.warehouse
    access_to_update.access_type = access.access_type

    db.commit()

    return access_to_update


@access_router.delete('/delete/{access_employee}')
def delete_access(access_employee:str, db: Session = Depends(get_session)):
    access_to_delete = db.query(models.Access).filter(models.Access.employee==access_employee).first()

    db.delete(access_to_delete)

    return access_to_delete