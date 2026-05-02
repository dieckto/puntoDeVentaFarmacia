# app/db/models.py
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship

from .session import Base

# ==========================================
# ENUMS
# ==========================================
class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"       # Gerente
    ATTENDANT = "ATTENDANT"   # Encargado / Cajero

# ==========================================
# RRHH Y SEGURIDAD
# ==========================================
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=True)  
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True) # Para Soft Delete

    user = relationship("User", back_populates="employee", uselist=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.ATTENDANT, nullable=False)
    is_active = Column(Boolean, default=True) # Para Soft Delete

    employee = relationship("Employee", back_populates="user")
    sales = relationship("Sale", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")

# ==========================================
# CATÁLOGOS EXTERNOS
# ==========================================
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    tax_id = Column(String, index=True, nullable=True)  
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    points = Column(Float, default=0.0) # Ajustado a Float para soportar decimales como en tus módulos
    is_active = Column(Boolean, default=True) # Para Soft Delete

    sales = relationship("Sale", back_populates="customer")

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    tax_id = Column(String, index=True, nullable=True)  
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True) # Para Soft Delete

    purchases = relationship("Purchase", back_populates="supplier")

# ==========================================
# INVENTARIO
# ==========================================
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True, nullable=True) # Hice nullable=True para que no te bloquee por ahora
    name = Column(String, nullable=False)
    description = Column(String, nullable=True) # Agregado para el módulo
    category = Column(String, nullable=True)
    unit_of_measure = Column(String, nullable=True)
    stock = Column(Integer, default=0)         # Renombrado de current_stock
    price_buy = Column(Float, default=0.0)     # Renombrado de purchase_price
    price_sell = Column(Float, default=0.0)    # Renombrado de sale_price
    is_active = Column(Boolean, default=True)  # Para Soft Delete

# ==========================================
# OPERACIONES: COMPRAS (ENTRADAS)
# ==========================================
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, index=True, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    status = Column(String, default="COMPLETED") # CRÍTICO: Para poder "Cancelar Compra"

    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True) # Nullable por si es compra sin proveedor registrado
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    supplier = relationship("Supplier", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
    details = relationship("PurchaseDetail", back_populates="purchase", cascade="all, delete-orphan")

class PurchaseDetail(Base):
    __tablename__ = "purchase_details"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=False) # Renombrado a unit_cost para match con schemas
    subtotal = Column(Float, nullable=False)

    purchase = relationship("Purchase", back_populates="details")
    medication = relationship("Medication")

# ==========================================
# OPERACIONES: VENTAS (SALIDAS)
# ==========================================
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, index=True, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    status = Column(String, default="COMPLETED") # CRÍTICO: Para poder "Cancelar Venta"

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    customer = relationship("Customer", back_populates="sales")
    user = relationship("User", back_populates="sales")
    details = relationship("SaleDetail", back_populates="sale", cascade="all, delete-orphan")

class SaleDetail(Base):
    __tablename__ = "sale_details"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False) 
    subtotal = Column(Float, nullable=False)

    sale = relationship("Sale", back_populates="details")
    medication = relationship("Medication")