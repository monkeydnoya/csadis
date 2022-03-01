from fastapi import APIRouter, Depends
from . import models
from .schemas import Invoice
from dbsession import get_session
from sqlalchemy.orm import Session


invoice_router = APIRouter(prefix='/invoice')


@invoice_router.get('/')
def get_invoice(db: Session = Depends(get_session)):
    invoices = db.query(models.Invoice).all()

    return invoices


@invoice_router.post('/create', response_model=Invoice)
def create_invoice(invoice: Invoice, db: Session = Depends(get_session)):
    invoice_to_create = models.Invoice(**invoice.dict())

    db.add(invoice_to_create)
    db.commit()

    return invoice_to_create


@invoice_router.put('/update/{invoice_id}', response_model=Invoice)
def update_invoice(invoice_id: int, invoice: Invoice, db: Session = Depends(get_session)):
    invoice_to_update = db.query(models.Invoice).filter(models.Invoice.id==invoice_id).first()
    invoice_to_update.number = invoice.number
    invoice_to_update.date = invoice.date
    invoice_to_update.employee = invoice.employee
    invoice_to_update.status = invoice.status
    invoice_to_update.type = invoice.type
    invoice_to_update.description = invoice.description
    invoice_to_update.item = invoice.item
    invoice_to_update.count = invoice.count

    db.commit()

    return invoice_to_update


@invoice_router.delete('/delete/{invoice_id}', response_model=Invoice)
def delete_invoice(invoice_id:int, invoice: Invoice, db: Session = Depends(get_session)):
    invoice_to_delete = db.query(models.Invoice).filter(models.Invoice.id==invoice_id).first()

    db.delete(invoice_to_delete)


    return invoice_to_delete