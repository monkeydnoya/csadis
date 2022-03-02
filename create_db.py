from database import Base,engine
from employee.models import Employee
from warehouse.models import WareHouse
from customer.models import Customer
from accesstype.models import AccessType
from invoice.models import Invoice


print('Creating databse ...')

Base.metadata.create_all(engine)