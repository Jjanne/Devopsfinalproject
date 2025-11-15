from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_session

router = APIRouter()

@router.get("/", response_model=List[schemas.CustomerRead])
def list_customers(db: Session = Depends(get_session)):
    return db.query(models.Customer).order_by(models.Customer.id.desc()).all()

@router.post("/", response_model=schemas.CustomerRead, status_code=201)
def create_customer(data: schemas.CustomerCreate, db: Session = Depends(get_session)):
    exists = db.query(models.Customer).filter(models.Customer.email == data.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    customer = models.Customer(**data.dict())
    db.add(customer)
    db.flush()
    return customer
