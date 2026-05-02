# app/modules/inventory/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.utils.auth import verify_token # Importamos el validador de JWT
from . import schemas, service

router = APIRouter(
    prefix="/inventory/medications", 
    tags=["Inventario y Medicamentos"],
    # Con esto protegemos TODAS las rutas de este router de golpe
    dependencies=[Depends(verify_token)] 
)

@router.get("/", response_model=List[schemas.MedicationResponse])
def list_medications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Buscar Medicamentos (Paginado) """
    return service.get_all_medications(db, skip=skip, limit=limit)

@router.get("/{med_id}", response_model=schemas.MedicationResponse)
def get_medication(med_id: int, db: Session = Depends(get_db)):
    """ Buscar un Medicamento específico por ID """
    return service.get_medication_by_id(db, med_id)

@router.post("/", response_model=schemas.MedicationResponse, status_code=201)
def create_medication(data: schemas.MedicationCreate, db: Session = Depends(get_db)):
    """ Alta de Medicamento """
    return service.create_medication(db, data)

@router.patch("/{med_id}", response_model=schemas.MedicationResponse)
def update_medication(med_id: int, data: schemas.MedicationUpdate, db: Session = Depends(get_db)):
    """ Editar Medicamento """
    return service.update_medication(db, med_id, data)

@router.delete("/{med_id}", status_code=200)
def delete_medication(med_id: int, db: Session = Depends(get_db)):
    """ Baja de Medicamento (Desactivación lógica) """
    return service.delete_medication(db, med_id)