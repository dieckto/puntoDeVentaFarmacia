from pydantic import BaseModel
from typing import Optional


class SupplierBase(BaseModel):
    tax_id: Optional[str] = None
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierResponse(SupplierBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class SupplierUpdate(BaseModel):
    tax_id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
