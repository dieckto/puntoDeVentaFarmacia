# app/modules/inventory/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Medication # Asegúrate de tener este modelo en tu app/db/models.py
from . import schemas

# BUSCAR / LISTAR
def get_all_medications(db: Session, skip: int = 0, limit: int = 100):
    # Solo traemos los activos, implementando paginación (skip/limit)
    return db.query(Medication).filter(Medication.is_active == True).offset(skip).limit(limit).all()

def get_medication_by_id(db: Session, med_id: int):
    med = db.query(Medication).filter(Medication.id == med_id, Medication.is_active == True).first()
    if not med:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    return med

# ALTA
def create_medication(db: Session, data: schemas.MedicationCreate):
    db_med = Medication(**data.model_dump())
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med

# EDITAR
def update_medication(db: Session, med_id: int, data: schemas.MedicationUpdate):
    db_med = get_medication_by_id(db, med_id)
    
    # Extraemos solo los campos que fueron enviados en la petición (no los nulos)
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_med, key, value)
        
    db.commit()
    db.refresh(db_med)
    return db_med

# BAJA (Soft Delete)
def delete_medication(db: Session, med_id: int):
    db_med = get_medication_by_id(db, med_id)
    db_med.is_active = False
    db.commit()
    return {"detail": "Medicamento dado de baja exitosamente"}