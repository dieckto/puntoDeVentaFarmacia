# app/modules/reports/service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime

from app.db.models import Sale, Purchase, Medication, Customer
from . import schemas

# 1. REPORTE DE VENTAS
def get_sales_report(db: Session) -> schemas.SalesReportResponse:
    # Filtramos solo ventas completadas
    completed_sales = db.query(Sale).filter(Sale.status == "COMPLETED")
    
    count = completed_sales.count()
    revenue = db.query(func.sum(Sale.total)).filter(Sale.status == "COMPLETED").scalar() or 0.0
    
    return schemas.SalesReportResponse(total_sales_count=count, total_revenue=revenue)

# 2. REPORTE DE COMPRAS
def get_purchases_report(db: Session) -> schemas.PurchasesReportResponse:
    completed_purchases = db.query(Purchase).filter(Purchase.status == "COMPLETED")
    
    count = completed_purchases.count()
    expenses = db.query(func.sum(Purchase.total)).filter(Purchase.status == "COMPLETED").scalar() or 0.0
    
    return schemas.PurchasesReportResponse(total_purchases_count=count, total_expenses=expenses)

# 3. REPORTE DE PRODUCTOS (Inventario)
def get_inventory_report(db: Session) -> schemas.InventoryReportResponse:
    active_meds = db.query(Medication).filter(Medication.is_active == True)
    
    count = active_meds.count()
    total_stock = db.query(func.sum(Medication.stock)).filter(Medication.is_active == True).scalar() or 0
    # Calculamos el valor potencial del inventario (stock * precio de venta)
    inventory_value = db.query(func.sum(Medication.stock * Medication.price_sell)).filter(Medication.is_active == True).scalar() or 0.0
    
    return schemas.InventoryReportResponse(
        total_products_active=count, 
        total_stock_items=total_stock, 
        total_inventory_value=inventory_value
    )

# 4. REPORTE DE CLIENTES
def get_customers_report(db: Session) -> schemas.CustomersReportResponse:
    active_customers = db.query(Customer).filter(Customer.is_active == True)
    count = active_customers.count()
    total_points = db.query(func.sum(Customer.points)).filter(Customer.is_active == True).scalar() or 0.0
    
    return schemas.CustomersReportResponse(total_active_customers=count, total_points_distributed=total_points)

# 5. REPORTE MENSUAL GENERAL (Conexión con los Procesos de PDF y Email)
def get_monthly_report(db: Session, year: int, month: int, export_pdf: bool = False, send_email: bool = False) -> schemas.MonthlyGeneralReportResponse:
    # Calculamos ingresos del mes específico
    revenue = db.query(func.sum(Sale.total)).filter(
        Sale.status == "COMPLETED",
        extract('year', Sale.created_at) == year,
        extract('month', Sale.created_at) == month
    ).scalar() or 0.0

    # Calculamos gastos del mes específico
    expenses = db.query(func.sum(Purchase.total)).filter(
        Purchase.status == "COMPLETED",
        extract('year', Purchase.created_at) == year,
        extract('month', Purchase.created_at) == month
    ).scalar() or 0.0

    profit = revenue - expenses
    message = "Reporte generado en JSON."

    # --- SIMULACIÓN DE PROCESOS INTERNOS (DIAGRAMA 3) ---
    if export_pdf:
        # Aquí llamarías a app.services.pdf_generator
        message += " PDF generado exitosamente."
        
    if send_email:
        # Aquí llamarías a app.services.email_sender
        message += " Enviado por correo al Gerente."

    return schemas.MonthlyGeneralReportResponse(
        month=month,
        year=year,
        revenue=revenue,
        expenses=expenses,
        profit=profit,
        message=message
    )