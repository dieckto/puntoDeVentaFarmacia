from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
# from app.utils.auth import verify_token  <-- Lo usaremos más adelante
from . import schemas, service

router = APIRouter(prefix="/users-employees", tags=["Recursos Humanos y Seguridad"])

# --- RUTAS DE EMPLEADOS ---
@router.get("/employees", response_model=List[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return service.get_all_employees(db)

@router.post("/employees", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return service.create_employee(data, db)

# --- RUTAS DE USUARIOS ---
@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return service.get_all_users(db)

@router.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(data, db)