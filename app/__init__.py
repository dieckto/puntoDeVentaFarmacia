from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importes de base de datos y utilidades
from app.db.session import engine, Base, SessionLocal
from app.db.models import User, Employee, UserRole # Importamos Empleado y el Enum de Rol
from app.utils.auth import get_password_hash

# IMPORTACIÓN DE LOS MÓDULOS (¡Todos listos y conectados!)
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.customers.router import router as customers_router
from app.modules.inventory.router import router as inventory_router
from app.modules.purchases.router import router as purchases_router
from app.modules.sales.router import router as sales_router
from app.modules.reports.router import router as reports_router


# 1. Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# 2. Inyectar usuario administrador por defecto (Seeding)
db = SessionLocal()
try:
    # Verificamos si ya existe el usuario "admin"
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    if not admin_user:
        # PASO A: Primero debemos crear su perfil de Empleado
        admin_employee = Employee(
            name="Administrador Principal", 
            position="Dueño/Gerente General"
        )
        db.add(admin_employee)
        db.flush() # Guardamos temporalmente para obtener el ID generado

        # PASO B: Ahora creamos el Usuario y lo ligamos al Empleado
        new_admin = User(
            employee_id=admin_employee.id,
            username="admin", 
            password_hash=get_password_hash("admin123"), # Cambia la contraseña en prod
            role=UserRole.ADMIN
        )
        db.add(new_admin)
        db.commit()
finally:
    db.close()


# 3. Instanciar FastAPI
app = FastAPI(
    title="API - Sistema de Farmacia y POS",
    description="Backend para gestión de inventario, compras, ventas y usuarios en farmacia.",
    version="1.0.0"
)

# 4. Configuración de CORS
origins =[
    "http://localhost:5173", # Puerto común para React/Vite/Vue
    "http://localhost:4200", # Puerto común para Angular
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En desarrollo permitimos todo. En prod usar 'origins'
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Inclusión de Routers Modulares
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(customers_router)
app.include_router(inventory_router)
app.include_router(purchases_router)
app.include_router(sales_router)
app.include_router(reports_router)

@app.get("/")
def health_check():
    return {
        "status": "online", 
        "service": "API Farmacia POS",
        "version": "1.0.0"
    }