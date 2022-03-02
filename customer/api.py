from fastapi import APIRouter, Depends
from . import models
from .schemas import Customer
from dbsession import get_session
from sqlalchemy.orm import Session


customer_router = APIRouter(prefix='/customer', tags=['customer'])


@customer_router.get('/')
def get_customer(db: Session = Depends(get_session)):
    customers = db.query(models.Customer).all()

    return customers


@customer_router.post('/create', response_model=Customer)
def create_customer(customer:Customer, db: Session = Depends(get_session)):
    customer_create = models.Customer(**customer.dict())

    db.add(customer_create)
    db.commit()

    return customer_create


@customer_router.put('/update/{customer_id}', response_model=Customer)
def update_customert(customer_id:int, customer:Customer, db: Session = Depends(get_session)):
    update_to_customer = db.query(models.Customer).filter(models.Customer.id==customer_id).first()
    update_to_customer.name = customer.name
    update_to_customer.address = customer.address

    db.commit()

    return update_to_customer


@customer_router.delete('/delete/{customer_id}',response_model=Customer)
def delete_customer(customer_id:int, db: Session = Depends(get_session)):
    customer_to_delete = db.query(models.Customer).filter(models.Customer.id == customer_id).first()

    db.delete(customer_to_delete)

    return customer_to_delete
