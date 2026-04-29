from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Employee, User
from .schemas import EmployeeCreate, UserCreate
from app.utils.auth import get_password_hash

# --- LÓGICA DE EMPLEADOS ---
def get_all_employees(db: Session):
    return db.query(Employee).all()

def create_employee(data: EmployeeCreate, db: Session):
    db_employee = Employee(**data.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# --- LÓGICA DE USUARIOS ---
def get_all_users(db: Session):
    return db.query(User).all()

def create_user(data: UserCreate, db: Session):
    # 1. Verificar que el username no exista
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    # 2. Verificar que el empleado exista
    existing_employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not existing_employee:
        raise HTTPException(status_code=404, detail="El ID de empleado no existe")

    # 3. Verificar que el empleado no tenga ya un usuario asignado (Relación 1:1)
    if existing_employee.user:
        raise HTTPException(status_code=400, detail="Este empleado ya tiene un usuario asignado")

    # 4. Encriptar la contraseña y guardar
    hashed_password = get_password_hash(data.password)
    
    db_user = User(
        employee_id=data.employee_id,
        username=data.username,
        password_hash=hashed_password,
        role=data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user