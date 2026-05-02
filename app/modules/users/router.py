from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
# 1. Descomentamos e importamos la función de autenticación
from app.utils.auth import verify_token  
from . import schemas, service

# 2. Añadimos la dependencia a nivel de router. 
# Esto protege automáticamente TODOS los endpoints definidos aquí abajo.
router = APIRouter(
    prefix="/users-employees", 
    tags=["Recursos Humanos y Seguridad"],
    dependencies=[Depends(verify_token)] # <--- ¡Seguridad activada!
)

# --- RUTAS DE EMPLEADOS ---
@router.get("/employees", response_model=List[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    """ Listar todos los empleados (Requiere Token) """
    return service.get_all_employees(db)

@router.post("/employees", response_model=schemas.EmployeeResponse, status_code=201)
def create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """ Registrar un nuevo empleado (Requiere Token) """
    return service.create_employee(data, db)

# --- RUTAS DE USUARIOS ---
@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    """ Listar todos los usuarios del sistema (Requiere Token) """
    return service.get_all_users(db)

@router.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Crear un usuario y vincularlo a un empleado (Requiere Token) """
    return service.create_user(data, db)

@router.patch("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    """ Diagrama 1: Editar Usuario """
    return service.update_user(db, user_id, data)

@router.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """ Diagrama 1: Eliminar Usuario """
    return service.delete_user(db, user_id)