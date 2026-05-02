# app/modules/purchases/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Purchase, PurchaseDetail, Medication
from . import schemas

# REGISTRAR COMPRA
def create_purchase(db: Session, purchase_data: schemas.PurchaseCreate, current_user_id: int):
    if not purchase_data.items:
        raise HTTPException(status_code=400, detail="La compra no puede estar vacía")

    total_amount = 0.0
    purchase_details_db =[]

    # Procesar cada artículo recibido del proveedor
    for item in purchase_data.items:
        med = db.query(Medication).filter(Medication.id == item.medication_id).first()
        if not med:
            raise HTTPException(status_code=404, detail=f"Medicamento ID {item.medication_id} no encontrado")

        # 1. PROCESO AUTOMÁTICO: Actualizar Stock (Suma)
        med.stock += item.quantity
        
        # 2. PROCESO AUTOMÁTICO: Actualizar Precio (Costo de compra)
        # Tu diagrama 6 lo menciona explícitamente. Si el proveedor subió el precio, lo actualizamos.
        med.price_buy = item.unit_cost

        subtotal = item.unit_cost * item.quantity
        total_amount += subtotal

        purchase_details_db.append(
            PurchaseDetail(
                medication_id=med.id,
                quantity=item.quantity,
                unit_cost=item.unit_cost,
                subtotal=subtotal
            )
        )

    # Crear la cabecera de la compra
    db_purchase = Purchase(
        user_id=current_user_id, # El Gerente/Admin que registró la compra
        supplier_id=purchase_data.supplier_id,
        total=total_amount,
        status="COMPLETED"
    )
    db.add(db_purchase)
    db.flush()

    # Vincular los detalles
    for detail in purchase_details_db:
        detail.purchase_id = db_purchase.id
        db.add(detail)

    db.commit()
    db.refresh(db_purchase)
    return db_purchase

# BUSCAR COMPRAS
def get_all_purchases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Purchase).order_by(Purchase.created_at.desc()).offset(skip).limit(limit).all()

def get_purchase_by_id(db: Session, purchase_id: int):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return purchase

# CANCELAR COMPRA (De tu Diagrama 6)
def cancel_purchase(db: Session, purchase_id: int):
    purchase = get_purchase_by_id(db, purchase_id)
    
    if purchase.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Esta compra ya fue cancelada previamente")
        
    # Lógica de reversión: Si cancelamos la compra, tenemos que RESTAR el stock que había entrado
    for detail in purchase.details:
        med = db.query(Medication).filter(Medication.id == detail.medication_id).first()
        if med:
            # Precaución: No dejar el stock en negativo si ya se vendió ese producto
            if med.stock >= detail.quantity:
                med.stock -= detail.quantity
            else:
                raise HTTPException(
                    status_code=400, 
                    detail=f"No se puede cancelar. El stock de {med.name} es insuficiente para revertir."
                )
                
    purchase.status = "CANCELLED"
    db.commit()
    db.refresh(purchase)
    return purchase