from fastapi import FastAPI
from database import SessionLocal
from employee.api import employee_router
from counteragent.api import counter_agent_router
from access.api import access_router
from accesstype.api import accesstype_router
from invoice.api import invoice_router
from items.api import items_router
from reserve.api import reserve_router

app = FastAPI()

# Dependency
# def get_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


app.include_router(employee_router)
app.include_router(counter_agent_router)
app.include_router(access_router)
app.include_router(accesstype_router)
app.include_router(invoice_router)
app.include_router(items_router)
app.include_router(reserve_router)