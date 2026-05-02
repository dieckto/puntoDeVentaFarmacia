# app/modules/purchases/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- ESQUEMAS PARA DETALLES DE COMPRA ---
class PurchaseDetailCreate(BaseModel):
    medication_id: int
    quantity: int
    unit_cost: float  # A cuánto nos vendió el proveedor esta vez

class PurchaseDetailResponse(BaseModel):
    id: int
    medication_id: int
    quantity: int
    unit_cost: float
    subtotal: float

    class Config:
        from_attributes = True

# --- ESQUEMAS PARA LA COMPRA (CABECERA) ---
class PurchaseCreate(BaseModel):
    # Si tienes tabla de proveedores, aquí va su ID. Lo dejamos opcional por si es compra rápida
    supplier_id: Optional[int] = None 
    items: List[PurchaseDetailCreate]

class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    supplier_id: Optional[int]
    total: float
    status: str # "COMPLETED", "CANCELLED"
    created_at: datetime
    details: List[PurchaseDetailResponse]

    class Config:
        from_attributes = True