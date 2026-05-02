# app/modules/auth/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import User
from app.utils.auth import verify_password, create_access_token

def authenticate_user(db: Session, username: str, password: str):
    # 1. Buscar al usuario en la base de datos
    user = db.query(User).filter(User.username == username).first()
    
    # 2. Si no existe o la contraseña no coincide, lanzamos error genérico (por seguridad)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Preparar los datos que irán dentro del JWT (Payload)
    # Usamos "sub" (subject) para el ID del usuario como recomienda el estándar JWT
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        # Si UserRole es un Enum, extraemos su valor (.value)
        "role": user.role.value if hasattr(user.role, 'value') else user.role 
    }
    
    # 4. Crear el token usando tu función de utils/auth.py
    access_token = create_access_token(token_data)
    
    # 5. Retornar el formato que espera nuestro TokenResponse
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": token_data["role"],
        "username": user.username
    }