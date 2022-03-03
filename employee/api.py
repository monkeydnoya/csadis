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


employee_logger = get_logger(__name__)
employee_router = APIRouter(prefix='/employee', tags=['employee'])

@employee_router.get('/')
def get_employees(Authorize: AuthJWT = Depends(),db: Session = Depends(get_session)):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        employee_logger.info(f'Autorized as {current_user}')

    except Exception as e:
        employee_logger.error('Invalid token')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token')

    current_user_access = db.query(models.Employee).filter(models.Employee.email==current_user).first()
    if current_user_access.post == 1:
        employees = db.query(models.Employee).all()
    
    else:
        employee_logger.error(f'Insufficient access level. Current access level: {current_user_access.post}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Insufficient access level. Current access level: {current_user_access.post}')

    return employees


@employee_router.put('/employee/{employee_id}', response_model=Employee)
def update_employee(employee_id:int,employee:Employee , db: Session = Depends(get_session)):
    employee_to_update = db.query(models.Employee).filter(models.Employee.id==employee_id).first()
    employee_to_update.name = employee.name
    employee_to_update.email = employee.email
    employee_to_update.password = employee.password
    employee_to_update.iin = employee.iin
    employee_to_update.post = employee.post

    db.commit()

    return employee_to_update


@employee_router.post('/signup', response_model=Employee)
def post_employee(employee:Employee, db: Session = Depends(get_session)):
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

    return new_employee


@employee_router.delete('/employee/{employee_id}')
def delete_employee(employee_id: int, db: Session = Depends(get_session)):
    employee_to_delete = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    db.delete(employee_to_delete)
    db.commit()

    return employee_to_delete


@employee_router.post('/login')
def login(employee: LoginModel, Authorize: AuthJWT=Depends(), db:Session = Depends(get_session)):
    db_employee = db.query(models.Employee).filter(models.Employee.email==employee.email).first()

    if db_employee and check_password_hash(db_employee.password,employee.password):
        access_token = Authorize.create_access_token(subject=db_employee.email)
        refresh_token = Authorize.create_refresh_token(subject=db_employee.email)

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        return jsonable_encoder(response)
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )