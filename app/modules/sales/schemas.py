# app/modules/sales/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- ESQUEMAS PARA LOS DETALLES (El "Carrito") ---
class SaleDetailCreate(BaseModel):
    medication_id: int
    quantity: int

class SaleDetailResponse(BaseModel):
    id: int
    medication_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True

# --- ESQUEMAS PARA LA VENTA PRINCIPAL (El "Ticket") ---
class SaleCreate(BaseModel):
    customer_id: Optional[int] = None  # Puede ser None si es un cliente de paso (Público General)
    discount: float = 0.0              # Para el "Aplicar Descuento 10" de tu diagrama
    items: List[SaleDetailCreate]      # Lista de medicamentos a vender

class SaleResponse(BaseModel):
    id: int
    user_id: int
    customer_id: Optional[int]
    total: float
    discount: float
    status: str
    created_at: datetime
    details: List[SaleDetailResponse]

    class Config:
        from_attributes = True