# Sistema de Punto de Venta para Farmacia (POS)

Un backend robusto y escalable desarrollado en **FastAPI** para la gestión integral de una farmacia. Incluye módulos para inventario, compras, ventas, usuarios, empleados, clientes y reportes, con autenticación JWT y base de datos SQLite (fácil migración a PostgreSQL/MySQL).

## 🚀 Características Principales

- **Gestión de Usuarios y Empleados**: Relación 1:1 entre empleados y usuarios, con roles (Admin, Manager, Attendant).
- **Inventario de Medicamentos**: Control de stock, precios de compra/venta y categorías.
- **Compras y Ventas**: Registro detallado de transacciones con proveedores y clientes, incluyendo puntos de recompensa.
- **Autenticación Segura**: Hashing de contraseñas con bcrypt y tokens JWT.
- **Arquitectura Modular**: Separación clara en capas (Router, Service, Schema, Models) para mantenibilidad.
- **API RESTful**: Endpoints bien documentados con FastAPI (Swagger UI incluido).
- **Docker Ready**: Configuración completa para desarrollo y despliegue con Docker Compose.
- **Base de Datos Relacional**: Modelos SQLAlchemy con relaciones complejas (1:1, 1:N, N:M).

## 🛠 Tecnologías Utilizadas

- **Backend**: FastAPI (framework asíncrono para APIs)
- **ORM**: SQLAlchemy (mapeo objeto-relacional)
- **Base de Datos**: SQLite (desarrollo); compatible con PostgreSQL/MySQL para producción
- **Autenticación**: PyJWT + bcrypt
- **Validación**: Pydantic (esquemas de datos)
- **Servidor**: Uvicorn (desarrollo) / Gunicorn (producción)
- **Contenedorización**: Docker + Docker Compose
- **Lenguaje**: Python 3.12+

## 📦 Instalación y Configuración

### Prerrequisitos
- Python 3.12+
- Docker y Docker Compose (opcional, recomendado para desarrollo)

### Opción 1: Usando Docker (Recomendado)
1. Clona el repositorio:
   ```bash
   git clone https://github.com/dieckto/puntoDeVentaFarmacia.git
   cd puntoDeVentaFarmacia
   ```

2. Construye y ejecuta con Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. La API estará disponible en: `http://localhost:8001`
   - Documentación interactiva (Swagger): `http://localhost:8001/docs`
   - ReDoc: `http://localhost:8001/redoc`

### Opción 2: Instalación Local
1. Clona el repositorio y navega al directorio.

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:
   ```bash
   uvicorn app.__init__:app --reload
   ```

5. Accede a la API en `http://127.0.0.1:8000`.

### Configuración Inicial
- **Usuario Admin por Defecto**: Al iniciar, se crea automáticamente un usuario `admin` con contraseña `admin123`. **Cambia la contraseña en producción**.
- **Base de Datos**: Se crea automáticamente en `./db_data/crm.db` (SQLite).

## 📁 Estructura del Proyecto

```
puntoDeVentaFarmacia/
├── app/
│   ├── __init__.py          # Inicialización de FastAPI, seeding de DB, CORS
│   ├── db/
│   │   ├── models.py        # Modelos SQLAlchemy (User, Employee, Medication, etc.)
│   │   └── session.py       # Configuración de DB (engine, session)
│   ├── modules/             # Módulos funcionales
│   │   ├── users/           # Gestión de empleados y usuarios
│   │   │   ├── router.py    # Endpoints API
│   │   │   ├── service.py   # Lógica de negocio
│   │   │   ├── schemas.py   # Validaciones Pydantic
│   │   │   └── models.py    # (Vacío; modelos globales en db/models.py)
│   │   ├── auth/            # (Pendiente: autenticación/login)
│   │   ├── inventory/       # (Pendiente: medicamentos)
│   │   ├── purchases/       # (Pendiente: compras a proveedores)
│   │   ├── sales/           # (Pendiente: ventas a clientes)
│   │   └── reports/         # (Pendiente: reportes y analytics)
│   ├── services/            # Servicios auxiliares (email, PDF)
│   └── utils/               # Utilidades (auth, db)
├── db_data/                 # Datos persistentes (SQLite)
├── docs/                    # Diagramas UML y documentación
├── Dockerfile               # Imagen Docker
├── docker-compose.yml       # Orquestación de contenedores
├── main.py                  # (Vacío; app en app/__init__.py)
├── requirements.txt         # Dependencias Python
└── README.md                # Este archivo
```

## 🔗 API Endpoints

### Salud del Sistema
- `GET /` - Verifica el estado de la API.

### Recursos Humanos (Users Module - Implementado)
- `GET /users-employees/employees` - Lista todos los empleados.
- `POST /users-employees/employees` - Crea un nuevo empleado.
- `GET /users-employees/users` - Lista todos los usuarios.
- `POST /users-employees/users` - Crea un nuevo usuario (ligado a un empleado).

**Ejemplo de Request (Crear Usuario)**:
```json
{
  "username": "jdoe",
  "password": "securepass",
  "role": "ATTENDANT",
  "employee_id": 1
}
```

### Módulos Pendientes
- **Auth**: Login/logout con JWT.
- **Inventory**: CRUD de medicamentos.
- **Purchases**: Registro de compras.
- **Sales**: Registro de ventas con cálculo de totales.
- **Reports**: Estadísticas y reportes.

## 🗄 Base de Datos

### Esquema Principal
- **Employees**: Información de empleados (1:1 con Users).
- **Users**: Credenciales y roles (Admin, Manager, Attendant).
- **Customers**: Clientes con puntos de recompensa.
- **Suppliers**: Proveedores.
- **Medications**: Inventario de medicamentos.
- **Purchases/PurchaseDetails**: Compras a proveedores.
- **Sales/SaleDetails**: Ventas a clientes.

### Relaciones
- Employee ↔ User (1:1)
- User → Sales/Purchases (1:N)
- Customer → Sales (1:N)
- Supplier → Purchases (1:N)
- Medication ↔ PurchaseDetails/SaleDetails (N:M)

### Migración a Producción
Cambia `SQLALCHEMY_DATABASE_URL` en `app/db/session.py` a PostgreSQL/MySQL. Ejemplo:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/farmacia_db"
```

## 🤝 Contribución

1. Forkea el repositorio.
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`.
3. Implementa cambios siguiendo la arquitectura modular.
4. Agrega tests si es posible.
5. Envía un Pull Request.

### Guías de Desarrollo
- Sigue PEP 8 para estilo de código.
- Usa commits descriptivos.
- Documenta endpoints con docstrings.
- Prueba con `docker-compose up` antes de push.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta `LICENSE` para más detalles.

## 📞 Contacto

- **Autor**: dieckto
- **Repositorio**: [GitHub](https://github.com/dieckto/puntoDeVentaFarmacia)
- **Issues**: Reporta bugs o solicita features en GitHub Issues.

---

¡Gracias por usar este sistema! Si tienes preguntas, abre un issue o contribuye al proyecto. 🚀" 
