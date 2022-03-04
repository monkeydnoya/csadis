from fastapi import FastAPI
from employee.api import employee_router
from warehouse.api import wh_router
from customer.api import customer_router
from accesstype.api import accesstype_router
from invoice.api import invoice_router
from items.api import items_router
from reserve.api import reserve_router
from fastapi_jwt_auth import AuthJWT
from employee.schemas import Settings
import inspect, re
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi


app = FastAPI()


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title = "Pizza Delivery API",
#         version = "1.0",
#         description = "An API for a Pizza Delivery Service",
#         routes = app.routes,
#     )

#     openapi_schema["components"]["securitySchemes"] = {
#         "Bearer Auth": {
#             "type": "apiKey",
#             "in": "header",
#             "name": "Authorization",
#             "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
#         }
#     }

#     # Get all routes where jwt_optional() or jwt_required
#     api_router = [route for route in app.routes if isinstance(route, APIRoute)]

#     for route in api_router:
#         path = getattr(route, "path")
#         endpoint = getattr(route,"endpoint")
#         methods = [method.lower() for method in getattr(route, "methods")]

#         for method in methods:
#             # access_token
#             if (
#                 re.search("jwt_required", inspect.getsource(endpoint)) or
#                 re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
#                 re.search("jwt_optional", inspect.getsource(endpoint))
#             ):
#                 openapi_schema["paths"][path][method]["security"] = [
#                     {
#                         "Bearer Auth": []
#                     }
#                 ]

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi


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

