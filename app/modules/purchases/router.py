# app/modules/purchases/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.utils.auth import verify_token
from . import schemas, service

router = APIRouter(
    prefix="/purchases", 
    tags=["Gestión de Compras (Proveedores)"],
    dependencies=[Depends(verify_token)]
)

@router.post("/", response_model=schemas.PurchaseResponse, status_code=201)
def registrar_compra(
    data: schemas.PurchaseCreate, 
    db: Session = Depends(get_db),
    current_user_id: str = Depends(verify_token) # Extraemos el ID desde JWT
):
    """ Ingresar medicamentos al inventario desde un proveedor """
    return service.create_purchase(db, data, int(current_user_id))

@router.get("/", response_model=List[schemas.PurchaseResponse])
def listar_compras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Ver historial de compras """
    return service.get_all_purchases(db, skip, limit)

@router.get("/{purchase_id}", response_model=schemas.PurchaseResponse)
def detalle_compra(purchase_id: int, db: Session = Depends(get_db)):
    """ Ver detalle de una compra por ID """
    return service.get_purchase_by_id(db, purchase_id)

@router.patch("/{purchase_id}/cancel", response_model=schemas.PurchaseResponse)
def cancelar_compra(purchase_id: int, db: Session = Depends(get_db)):
    """ Cancelar una compra (Revierte el stock ingresado) """
    return service.cancel_purchase(db, purchase_id) 