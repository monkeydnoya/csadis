from database import Base,engine
from employee.models import Employee
from counteragent.models import CounterAgent
from access.models import Access
from accesstype.models import AccessType
from invoice.models import Invoice


print('Creating databse ...')

Base.metadata.create_all(engine)