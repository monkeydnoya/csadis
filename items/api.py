from fastapi import APIRouter, Depends
from . import models
from .schemas import Items
from sqlalchemy.orm import Session
from dbsession import get_session


items_router = APIRouter(prefix='/items')


@items_router.get('/')
def get_items(db: Session = Depends(get_session)):
    items = db.query(models.Items).all()

    return items


@items_router.post('/create', response_model=Items)
def create_items(items: Items, db: Session = Depends(get_session)):
    items_to_create = models.Items(**items.dict())

    db.add(items_to_create)
    db.commit()

    return items_to_create


@items_router.put('/update/{item_id}', response_model=Items)
def update_items(item_id: int, items: Items, db: Session = Depends(get_session)):
    items_to_update = db.query(models.Items).filter(models.Items.id==item_id).first()
    items_to_update.name = items.name
    items_to_update.type = items.type
    items_to_update.price = items.price
    items_to_update.currency = items.currency

    db.commit()

    return items_to_update


@items_router.delete('/delete/{item_id}',response_model=Items)
def delete_item(itemd_id: int, items: Items, db: Session = Depends(get_session)):
    item_to_delete = db.query(models.Items).filter(models.Items.id==items.id).firs()

    db.delete(item_to_delete)

    return item_to_delete