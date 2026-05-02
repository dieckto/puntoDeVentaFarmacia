# app/modules/auth/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.db import get_db
from . import schemas, service

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=schemas.TokenResponse)
def login_for_access_token(
    # OAuth2PasswordRequestForm captura "username" y "password" de un form-data.
    # ¡Esto hace que el botón candado verde de Swagger UI funcione!
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Inicia sesión y obtén un token JWT.
    """
    return service.authenticate_user(db, form_data.username, form_data.password)