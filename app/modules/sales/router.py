# app/modules/sales/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.utils.auth import verify_token
from . import schemas, service

router = APIRouter(
    prefix="/sales", 
    tags=["Gestión de Ventas"],
    dependencies=[Depends(verify_token)]
)

@router.post("/", response_model=schemas.SaleResponse, status_code=201)
def registrar_venta(
    data: schemas.SaleCreate, 
    db: Session = Depends(get_db),
    current_user_id: str = Depends(verify_token) # Extraemos quién es el cajero desde el JWT
):
    """ Registrar una nueva Venta """
    # Convertimos el string del token a entero
    user_id = int(current_user_id)
    return service.create_sale(db, data, user_id)

@router.get("/", response_model=List[schemas.SaleResponse])
def listar_ventas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Buscar historial de Ventas """
    return service.get_all_sales(db, skip, limit)

@router.get("/{sale_id}", response_model=schemas.SaleResponse)
def detalle_venta(sale_id: int, db: Session = Depends(get_db)):
    """ Ver el detalle de una Venta específica """
    return service.get_sale_by_id(db, sale_id)


@router.patch("/{sale_id}/cancel", response_model=schemas.SaleResponse)
def cancelar_venta(sale_id: int, db: Session = Depends(get_db)):
    """ 
    Diagrama 5: Cancelar Venta 
    (Revierte el stock y resta los puntos de recompensa al cliente)
    """
    return service.cancel_sale(db, sale_id)