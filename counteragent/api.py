from . import models
from fastapi import APIRouter, Depends
from .schemas import CounterAgent
from dbsession import get_session
from sqlalchemy.orm import Session


counter_agent_router = APIRouter(prefix='/counter-agent', tags=['counter-agent'])


@counter_agent_router.get('/')
def get_counter_agents(db: Session = Depends(get_session)):
    counter_agents = db.query(models.CounterAgent).all()

    return counter_agents


@counter_agent_router.post('/create', response_model=CounterAgent)
def create_counter_agent(counter_agent:CounterAgent, db: Session = Depends(get_session)):
    counter_agent_create = models.CounterAgent(**counter_agent.dict())

    db.add(counter_agent_create)
    db.commit()

    return counter_agent_create


@counter_agent_router.put('/update/counter_agent_id', response_model=CounterAgent)
def update_counter_agent(counter_agent_id:int, counter_agent:CounterAgent, db: Session = Depends(get_session)):
    update_to_counter_agent = db.query(models.CounterAgent).filter(models.CounterAgent.id==counter_agent_id).first()
    update_to_counter_agent.name = counter_agent.name
    update_to_counter_agent.address = counter_agent.address
    update_to_counter_agent.type = counter_agent.type

    db.commit()

    return update_to_counter_agent


@counter_agent_router.delete('/delete/{counter_agent_id}',response_model=CounterAgent)
def delete_counter_agent(counter_agent_id:int, db: Session = Depends(get_session)):
    counter_agent_to_delete = db.query(models.CounterAgent).filter(models.CounterAgent.id == counter_agent_id).first()

    db.delete(counter_agent_to_delete)

    return counter_agent_to_delete
