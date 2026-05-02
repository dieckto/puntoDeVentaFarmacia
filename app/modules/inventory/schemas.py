# app/modules/inventory/schemas.py
from pydantic import BaseModel
from typing import Optional

class MedicationBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_buy: float # Precio al que compramos al proveedor
    price_sell: float # Precio al público
    stock: int = 0
    category: Optional[str] = None

class MedicationCreate(MedicationBase):
    pass

class MedicationUpdate(BaseModel):
    # Todos opcionales porque podemos editar solo 1 campo a la vez
    name: Optional[str] = None
    description: Optional[str] = None
    price_buy: Optional[float] = None
    price_sell: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class MedicationResponse(MedicationBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True