from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from . import models
from .schemas import Employee, LoginModel
from dbsession import get_session
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from log_config import get_logger
from check import check_authorization_token, insufficient_access_level


employee_logger = get_logger(__name__)
employee_router = APIRouter(prefix='/employee', tags=['employee'])
# def check_authorization_token(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         current_user = Authorize.get_jwt_subject()
#         employee_logger.info(f'Autorized success. User: {current_user}')
#         return current_user

#     except Exception as e:
#         employee_logger.error('Invalid token')
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token')


# def insufficient_access_level(method):
#     employee_logger.error(f'{method} request error: Insufficient access level.')
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Insufficient access level')


@employee_router.get('/')
async def get_employees(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'GET'
    current_user = check_authorization_token(employee_logger,Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email==current_user).first()

    if current_user_access.post >= 1:
        employees = db.query(models.Employee).all()
        employee_logger.info(f'GET request to localhost:8000/employee was executed successfully. Request was made by {current_user}')
    
    else:
        insufficient_access_level(employee_logger, method)

    return employees


@employee_router.get('/{employee_id}')
def get_employees(employee_id: int,Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = f'GET BY ID {employee_id}'
    current_user = check_authorization_token(employee_logger,Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email==current_user).first()

    if current_user_access.post >= 1:
        employees = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
        employee_logger.info(f'GET request to localhost:8000/employee/{employee_id} was executed successfully. Request was made by {current_user}')
    
    else:
        insufficient_access_level(employee_logger, method)

    return employees



@employee_router.put('/employee/{employee_id}', response_model=Employee)
def update_employee(employee_id:int,employee:Employee , Authorize:AuthJWT = Depends(),db: Session = Depends(get_session)):
    method = 'PUT'

    current_user = check_authorization_token(employee_logger, Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email==current_user).first()
    
    if current_user_access.post >= 2:
        employee_to_update = db.query(models.Employee).filter(models.Employee.id==employee_id).first()
        employee_to_update.name = employee.name
        employee_to_update.email = employee.email
        employee_to_update.password = employee.password
        employee_to_update.iin = employee.iin
        employee_to_update.post = employee.post
        
        db.commit()

        employee_logger.info(f'PUT request to localhost:8000/employee was executed successfully. Request was made by {current_user}')

    else:
        insufficient_access_level(employee_logger, method)

    return employee_to_update


@employee_router.post('/signup', response_model=Employee)
def post_employee(employee:Employee, Authorize: AuthJWT = Depends() ,db: Session = Depends(get_session)):
    method = 'POST'
    current_user = check_authorization_token(employee_logger, Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email==current_user).first()
    
    if current_user_access.post >= 2:
        db_email = db.query(models.Employee).filter(models.Employee.email==employee.email).first()
        db_iin = db.query(models.Employee).filter(models.Employee.iin==employee.iin).first()


        if db_email is not None:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = 'User with the email already exists'
                )
        
        if db_iin is not None:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = 'User with the iin already exists'
                )

        new_employee = models.Employee(
            id = employee.id,
            name = employee.name,
            email = employee.email,
            password = generate_password_hash(employee.password),
            iin = employee.iin,
            post = employee.post
        )

        db.add(new_employee)
        db.commit()

    else:
        insufficient_access_level(employee_logger, method)

    return new_employee


@employee_router.delete('/delete/{employee_id}')
def delete_employee(employee_id: int, Authorize: AuthJWT = Depends() , db: Session = Depends(get_session)):
    method = 'DELETE'
    current_user = check_authorization_token(employee_logger, Authorize)
    current_user_access = db.query(models.Employee).filter(models.Employee.email==current_user).first()

    if current_user_access.post >= 2:
        employee_to_delete = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

        db.delete(employee_to_delete)
        db.commit()

    else:
        insufficient_access_level(employee_logger, method)

    return employee_to_delete


@employee_router.post('/login')
async def login(employee: LoginModel, Authorize: AuthJWT=Depends(), db:Session = Depends(get_session)):
    db_employee = db.query(models.Employee).filter(models.Employee.email==employee.email).first()

    if db_employee and check_password_hash(db_employee.password,employee.password):
        access_token = Authorize.create_access_token(subject=db_employee.email)
        # refresh_token = Authorize.create_refresh_token(subject=db_employee.email)

        response = {
            'access': access_token
            # 'refresh': refresh_token
        }

        return jsonable_encoder(response)
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )


# @employee_router.get('/refresh')
# def refresh_token(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = 'Please provide a valid refresh token')
    
#     current_user = Authorize.get_jwt_subject()


#     access_token = Authorize.create_access_token(subject=current_user)

#     return jsonable_encoder({'access':access_token })