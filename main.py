from fastapi import FastAPI
from database import SessionLocal
from employee.api import employee_router
from warehouse.api import wh_router
from customer.api import customer_router
from accesstype.api import accesstype_router
from invoice.api import invoice_router
from items.api import items_router
from reserve.api import reserve_router
from fastapi_jwt_auth import AuthJWT
from employee.schemas import Settings


app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()
    
# Dependency
# def get_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


app.include_router(employee_router)
app.include_router(wh_router)
app.include_router(customer_router)
app.include_router(accesstype_router)
app.include_router(invoice_router)
app.include_router(items_router)
app.include_router(reserve_router)