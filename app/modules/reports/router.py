# app/modules/reports/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.utils.db import get_db
from app.utils.auth import verify_token
from . import schemas, service

router = APIRouter(
    prefix="/reports", 
    tags=["Reportes y Estadísticas"],
    dependencies=[Depends(verify_token)] # <-- Restringido a usuarios logueados (Admin/Gerente)
)

@router.get("/sales", response_model=schemas.SalesReportResponse)
def reporte_ventas(db: Session = Depends(get_db)):
    """ Diagrama 3: Reporte de Ventas """
    return service.get_sales_report(db)

@router.get("/purchases", response_model=schemas.PurchasesReportResponse)
def reporte_compras(db: Session = Depends(get_db)):
    """ Diagrama 3: Reporte de Compras """
    return service.get_purchases_report(db)

@router.get("/inventory", response_model=schemas.InventoryReportResponse)
def reporte_productos(db: Session = Depends(get_db)):
    """ Diagrama 3: Reporte de Productos """
    return service.get_inventory_report(db)

@router.get("/customers", response_model=schemas.CustomersReportResponse)
def reporte_clientes(db: Session = Depends(get_db)):
    """ Diagrama 3: Reporte de Clientes """
    return service.get_customers_report(db)

@router.get("/monthly", response_model=schemas.MonthlyGeneralReportResponse)
def reporte_mensual_general(
    year: int = datetime.now().year, 
    month: int = datetime.now().month, 
    export_pdf: bool = False, 
    send_email: bool = False, 
    db: Session = Depends(get_db)
):
    """ 
    Diagrama 3: Reporte Mensual General.
    Incluye flags opcionales para disparar los procesos internos de PDF y Correo.
    """
    return service.get_monthly_report(db, year, month, export_pdf, send_email)