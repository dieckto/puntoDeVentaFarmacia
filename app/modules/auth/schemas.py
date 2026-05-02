# app/modules/auth/schemas.py
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # Añadimos estos campos para que el frontend sepa quién se logueó
    # y qué menú o pantallas mostrarle (Admin, Gerente, Encargado)
    role: str 
    username: str