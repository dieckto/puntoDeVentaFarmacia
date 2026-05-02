# app/modules/customers/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.utils.auth import verify_token
from . import schemas, service

router = APIRouter(
    prefix="/customers", 
    tags=["Gestión de Clientes"],
    dependencies=[Depends(verify_token)] # <-- Seguridad habilitada
)

@router.get("/", response_model=List[schemas.CustomerResponse])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Buscar todos los Clientes (Encargado, Gerente, Admin) """
    return service.get_all_customers(db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=schemas.CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """ Buscar un Cliente por ID """
    return service.get_customer_by_id(db, customer_id)

@router.post("/", response_model=schemas.CustomerResponse, status_code=201)
def create_customer(data: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """ Registrar nuevo Cliente """
    return service.create_customer(db, data)

@router.patch("/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer(customer_id: int, data: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    """ Editar datos del Cliente """
    return service.update_customer(db, customer_id, data)

@router.delete("/{customer_id}", status_code=200)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """ Eliminar Cliente (Soft Delete) """
    return service.delete_customer(db, customer_id)