from email.errors import InvalidMultipartContentTransferEncodingDefect
from fastapi import APIRouter, Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from . import models
from employee.models import Employee
from .schemas import Invoice
from dbsession import get_session
from sqlalchemy.orm import Session
from log_config import get_logger
from check import *

invoice_logger = get_logger(__name__)
invoice_router = APIRouter(prefix='/invoice', tags=['invoice'])


@invoice_router.get('/')
def get_invoice(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'
    current_user = check_authorization_token(invoice_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        invoices = db.query(models.Invoice).all()
        invoice_logger.info(f"{method} request to localhost:8000/invoice was executed successfully. Request was made by {current_user}")

    else:
        insufficient_access_level(invoice_logger, method)

    return invoices

@invoice_router.get('/{invoice_id}')
def get_invoice_by_id(invoice_id: int,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = f'GET BY ID {invoice_id}'
    current_user = check_authorization_token(invoice_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 1 or current_user_access.post == 3:
        invoice_by_id = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
        invoice_logger.info(f"{method} request to localhost:8000/invoice/{invoice_id} was executed successfully. Request was made by {current_user}")

    else:
        insufficient_access_level(invoice_logger, method)

    return invoice_by_id

@invoice_router.post('/create', response_model=Invoice)
def create_invoice(invoice: Invoice,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'POST'
    current_user = check_authorization_token(invoice_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 1 or current_user_access.post == 3:
        invoice_to_create = models.Invoice(**invoice.dict())

        db.add(invoice_to_create)
        db.commit()
        invoice_logger.info(f"{method} request to localhost:8000/invoice/create was executed successfully. Request was made by {current_user}")
    
    else:
        insufficient_access_level(invoice_logger, method)

    return invoice_to_create


@invoice_router.put('/update/{invoice_id}', response_model=Invoice)
def update_invoice(invoice_id: int, invoice: Invoice,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'PUT'
    current_user = check_authorization_token(invoice_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        invoice_to_update = db.query(models.Invoice).filter(models.Invoice.id==invoice_id).first()
        invoice_to_update.number = invoice.number
        invoice_to_update.date = invoice.date
        invoice_to_update.employee = invoice.employee
        invoice_to_update.status = invoice.status
        invoice_to_update.type = invoice.type
        invoice_to_update.description = invoice.description
        invoice_to_update.warehouse = invoice.warehouse
        invoice_to_update.item = invoice.item
        invoice_to_update.count = invoice.count

        db.commit()

        invoice_logger.info(f"{method} request to localhost:8000/invoice//update/{invoice_id} was executed successfully. Request was made by {current_user}")
    
    else:
        insufficient_access_level(invoice_logger, method)

    return invoice_to_update


@invoice_router.delete('/delete/{invoice_id}', response_model=Invoice)
def delete_invoice(invoice_id:int, invoice: Invoice,Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'DELETE'
    current_user = check_authorization_token(invoice_logger, Authorize)
    current_user_access = db.query(Employee).filter(Employee.email == current_user).first()

    if current_user_access.post == 3:
        invoice_to_delete = db.query(models.Invoice).filter(models.Invoice.id==invoice_id).first()

        db.delete(invoice_to_delete)

        invoice_logger.info(f"{method} request to localhost:8000/invoice//delete/{invoice_id} was executed successfully. Request was made by {current_user}")
    
    else:
        insufficient_access_level(invoice_logger, method)

    return invoice_to_delete