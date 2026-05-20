from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Supplier
from . import schemas


def get_all_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Supplier).filter(Supplier.is_active == True).offset(skip).limit(limit).all()


def get_supplier_by_id(db: Session, supplier_id: int):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.is_active == True).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return supplier


def create_supplier(db: Session, data: schemas.SupplierCreate, current_user_id: int):
    if data.tax_id:
        existing = db.query(Supplier).filter(Supplier.tax_id == data.tax_id, Supplier.is_active == True).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un proveedor con esa identificación fiscal")

    db_supplier = Supplier(**data.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def update_supplier(db: Session, supplier_id: int, data: schemas.SupplierUpdate):
    supplier = get_supplier_by_id(db, supplier_id)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(supplier, key, value)

    db.commit()
    db.refresh(supplier)
    return supplier


def delete_supplier(db: Session, supplier_id: int):
    supplier = get_supplier_by_id(db, supplier_id)
    supplier.is_active = False
    db.commit()
    return {"detail": "Proveedor eliminado exitosamente"}
