from database import Base,engine
from employee.models import Employee
from counteragent.models import CounterAgent


print('Creating databse ...')

Base.metadata.create_all(engine)