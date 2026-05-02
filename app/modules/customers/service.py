# app/modules/customers/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Customer # Asegúrate de tener este modelo
from . import schemas

# BUSCAR / LISTAR
def get_all_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).filter(Customer.is_active == True).offset(skip).limit(limit).all()

def get_customer_by_id(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.is_active == True).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return customer

# REGISTRAR (ALTA)
def create_customer(db: Session, data: schemas.CustomerCreate):
    # Verificamos si el email o teléfono ya existen para evitar duplicados molestos
    if data.email:
        existing = db.query(Customer).filter(Customer.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Este correo ya está registrado")
            
    db_customer = Customer(**data.model_dump())
    # Los puntos se inician en 0 automáticamente desde la definición del modelo en models.py
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# EDITAR
def update_customer(db: Session, customer_id: int, data: schemas.CustomerUpdate):
    db_customer = get_customer_by_id(db, customer_id)
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_customer, key, value)
        
    db.commit()
    db.refresh(db_customer)
    return db_customer

# ELIMINAR (BAJA)
def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer_by_id(db, customer_id)
    db_customer.is_active = False
    db.commit()
    return {"detail": "Cliente eliminado exitosamente"}