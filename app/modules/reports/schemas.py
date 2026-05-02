# app/modules/reports/schemas.py
from pydantic import BaseModel
from typing import Optional

class SalesReportResponse(BaseModel):
    total_sales_count: int
    total_revenue: float
    # Podrías añadir más cosas en el futuro como "top_selling_product"

class PurchasesReportResponse(BaseModel):
    total_purchases_count: int
    total_expenses: float

class InventoryReportResponse(BaseModel):
    total_products_active: int
    total_stock_items: int
    total_inventory_value: float # Valor total del stock si vendiéramos todo

class CustomersReportResponse(BaseModel):
    total_active_customers: int
    total_points_distributed: float

class MonthlyGeneralReportResponse(BaseModel):
    month: int
    year: int
    revenue: float
    expenses: float
    profit: float # Ganancia (Ventas - Compras)
    message: Optional[str] = None # Para indicar si se envió por correo o generó PDF