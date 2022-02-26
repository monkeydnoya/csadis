import models
from fastapi import Depends,APIRouter
from schemas import Employee
from main import get_session
from sqlalchemy.orm import Session

employee_router = APIRouter(prefix='/followers', tags=['followers'])

@employee_router.get('/employees')
def get_employees(db: Session = Depends(get_session)):
    employees = db.query(models.Employee).all()

    return employees


@employee_router.put('/employee/{employee_id}', response_model=Employee)
def update_employee(employee_id:int,employee:Employee , db: Session = Depends(get_session)):
    employee_to_update = db.query(models.Employee).filter(models.Employee.id==employee_id).first()
    employee_to_update.name = employee.name
    employee_to_update.warehouse = employee.warehouse
    employee_to_update.iin = employee.iin
    employee_to_update.post = employee.post

    db.commit()

    return employee_to_update


@employee_router.post('/employeecreate', response_model=Employee)
def post_employee(employee:Employee, db: Session = Depends(get_session)):
    employee_to_post = models.Employee(**employee.dict())

    db.add(employee_to_post)
    db.commit()

    return employee_to_post


@employee_router.delete('/employee/{employee_id}')
def delete_employee(employee_id: int, db: Session = Depends(get_session)):
    employee_to_delete = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    db.delete(employee_to_delete)
    db.commit()

    return employee_to_delete


