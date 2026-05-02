# app/modules/sales/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Sale, SaleDetail, Medication, Customer
from . import schemas

def create_sale(db: Session, sale_data: schemas.SaleCreate, current_user_id: int):
    # 1. Validar que la lista de items no esté vacía
    if not sale_data.items:
        raise HTTPException(status_code=400, detail="La venta no puede estar vacía")

    total_amount = 0.0
    sale_details_db =[]

    # 2. Procesar cada medicamento del carrito
    for item in sale_data.items:
        med = db.query(Medication).filter(Medication.id == item.medication_id, Medication.is_active == True).first()
        
        if not med:
            raise HTTPException(status_code=404, detail=f"Medicamento ID {item.medication_id} no encontrado")
        
        # Validación de Stock (Regla de negocio crítica)
        if med.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para {med.name}. Stock actual: {med.stock}"
            )

        # Calcular subtotal asegurando que usamos el precio de la BD (evita hackeos desde el frontend)
        subtotal = med.price_sell * item.quantity
        total_amount += subtotal

        # ACTUALIZAR STOCK (Proceso de tu Diagrama 5)
        med.stock -= item.quantity

        # Preparar el detalle de la venta
        sale_details_db.append(
            SaleDetail(
                medication_id=med.id,
                quantity=item.quantity,
                unit_price=med.price_sell,
                subtotal=subtotal
            )
        )

    # 3. Aplicar descuento (Proceso de tu Diagrama 5: "Aplicar Descuento 10")
    if sale_data.discount > 0:
        total_amount -= sale_data.discount
        if total_amount < 0:
            total_amount = 0

    # 4. ACTUALIZAR PUNTOS DEL CLIENTE (Proceso de tu Diagrama 5)
    if sale_data.customer_id:
        customer = db.query(Customer).filter(Customer.id == sale_data.customer_id, Customer.is_active == True).first()
        if customer:
            # Ejemplo: Otorgamos 1 punto por cada $10 gastados
            puntos_ganados = total_amount / 10.0
            customer.points += puntos_ganados

    # 5. Guardar la Venta (Cabecera)
    db_sale = Sale(
        user_id=current_user_id, # El empleado que está cobrando
        customer_id=sale_data.customer_id,
        total=total_amount,
        discount=sale_data.discount,
        status="COMPLETED"
    )
    db.add(db_sale)
    db.flush() # flush() nos da el db_sale.id sin hacer commit todavía

    # 6. Guardar los Detalles vinculados a la venta
    for detail in sale_details_db:
        detail.sale_id = db_sale.id
        db.add(detail)

    # 7. COMMIT FINAL: Si algo falló arriba, nada de esto se guarda (Transacción segura)
    db.commit()
    db.refresh(db_sale)
    
    return db_sale

# BUSCAR / LISTAR VENTAS
def get_all_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sale).order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()

def get_sale_by_id(db: Session, sale_id: int):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return sale

# Agregar en app/modules/sales/service.py

# CANCELAR VENTA
def cancel_sale(db: Session, sale_id: int):
    sale = get_sale_by_id(db, sale_id)
    
    if sale.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Esta venta ya está cancelada")

    # 1. MAGIA INVERSA: Regresar el stock al inventario
    for detail in sale.details:
        med = db.query(Medication).filter(Medication.id == detail.medication_id).first()
        if med:
            med.stock += detail.quantity # Devolvemos las cajas al estante

    # 2. MAGIA INVERSA: Quitarle los puntos al cliente (para que no haga trampa)
    if sale.customer_id:
        customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
        if customer:
            puntos_a_restar = sale.total / 10.0
            customer.points -= puntos_a_restar
            # Evitar que los puntos queden en negativo si ya los había gastado
            if customer.points < 0:
                customer.points = 0

    # 3. Cambiar el estatus
    sale.status = "CANCELLED"
    db.commit()
    db.refresh(sale)
    
    return sale