from pydantic import BaseModel
from typing import Optional
from app.db.models import UserRole

# --- ESQUEMAS PARA EMPLEADO ---
class EmployeeBase(BaseModel):
    name: str
    position: Optional[str] = None
    phone: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS PARA USUARIO ---
class UserBase(BaseModel):
    username: str
    role: UserRole
    employee_id: int

class UserCreate(UserBase):
    password: str # Recibe el password en texto plano para el registro

class UserResponse(UserBase):
    id: int
    # Opcional: Anidamos los datos del empleado para que el frontend lo tenga a la mano
    employee: Optional[EmployeeResponse] = None 
    
    class Config:
        from_attributes = True