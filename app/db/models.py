# app/db/models.py
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

# Importamos el Base desde tu archivo de configuración
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
    position = Column(String)  # Puesto
    phone = Column(String)

    # Relación 1 a 1 con User
    user = relationship("User", back_populates="employee", uselist=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.ATTENDANT, nullable=False)

    employee = relationship("Employee", back_populates="user")
    
    # Relaciones hacia las transacciones que ha realizado este usuario
    sales = relationship("Sale", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")


# ==========================================
# CATÁLOGOS EXTERNOS
# ==========================================
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    tax_id = Column(String, index=True)  # RFC
    name = Column(String, nullable=False)
    email = Column(String)
    birth_date = Column(Date)
    reward_points = Column(Integer, default=0) # Puntos acumulados

    sales = relationship("Sale", back_populates="customer")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    tax_id = Column(String, index=True)  # RFC / NIT
    name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    email = Column(String)

    purchases = relationship("Purchase", back_populates="supplier")


# ==========================================
# INVENTARIO
# ==========================================
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True, nullable=False) # Código de barras/SKU
    name = Column(String, nullable=False)
    category = Column(String)
    unit_of_measure = Column(String)
    current_stock = Column(Integer, default=0)
    purchase_price = Column(Float, default=0.0)
    sale_price = Column(Float, default=0.0)


# ==========================================
# OPERACIONES: COMPRAS (ENTRADAS)
# ==========================================
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, index=True) # Folio de la factura del proveedor
    created_at = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    notes = Column(Text)

    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
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
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    purchase = relationship("Purchase", back_populates="details")
    medication = relationship("Medication")


# ==========================================
# OPERACIONES: VENTAS (SALIDAS)
# ==========================================
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, index=True) # Folio para el cliente
    created_at = Column(DateTime, default=datetime.utcnow)
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    points_generated = Column(Integer, default=0)
    notes = Column(Text)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True) # Nullable para ventas al público en general
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
    unit_price = Column(Float, nullable=False) # Guardamos el precio histórico
    subtotal = Column(Float, nullable=False)

    sale = relationship("Sale", back_populates="details")
    medication = relationship("Medication")