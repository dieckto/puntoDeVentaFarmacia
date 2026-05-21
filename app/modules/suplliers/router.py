# app/modules/suplliers/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.utils.auth import verify_token
from . import schemas, service

router = APIRouter(
    prefix="/suppliers", 
    tags=["Gestión de Proveedores"],
    dependencies=[Depends(verify_token)]
)

@router.post("/", response_model=schemas.SupplierResponse, status_code=201)
def registrar_proveedor(
    data: schemas.SupplierCreate, 
    db: Session = Depends(get_db),
    current_user_id: str = Depends(verify_token) # Extraemos quién es el gerente desde el JWT
):
    """ Registrar un nuevo Proveedor """
    # Convertimos el string del token a entero
    user_id = int(current_user_id)
    return service.create_supplier(db, data, user_id)   

@router.get("/", response_model=List[schemas.SupplierResponse])
def listar_proveedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Listar Proveedores registrados """
    return service.get_all_suppliers(db, skip, limit) 

@router.put("/{supplier_id}", response_model=schemas.SupplierResponse)
def actualizar_proveedor(supplier_id: int, data: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    """ Actualizar la información de un Proveedor """
    return service.update_supplier(db, supplier_id, data)   


@router.delete("/{supplier_id}", status_code=200)
def eliminar_proveedor(supplier_id: int, db: Session = Depends(get_db)):
    """ Eliminar un Proveedor (Soft Delete) """
    return service.delete_supplier(db, supplier_id) 

@router.get("/{supplier_id}", response_model=schemas.SupplierResponse)
def detalle_proveedor(supplier_id: int, db: Session = Depends(get_db)):
    """ Ver el detalle de un Proveedor específico """
    return service.get_supplier_by_id(db, supplier_id)  

