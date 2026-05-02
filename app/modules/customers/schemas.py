# app/modules/customers/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None # Valida que sea un correo con formato correcto

class CustomerCreate(CustomerBase):
    pass # Al crear, los puntos inician en 0 por defecto en la BD

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    # No permitimos actualizar 'points' desde aquí, eso lo hará 
    # el sistema de Ventas automáticamente (como indica tu diagrama).

class CustomerResponse(CustomerBase):
    id: int
    points: float
    is_active: bool

    class Config:
        from_attributes = True