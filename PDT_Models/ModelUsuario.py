from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class ModelUsuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Debe contener solo letras y espacios.")
    apellido: str = Field(..., min_length=3, max_length=50, description="Debe contener solo letras y espacios.")
    email: EmailStr = Field(..., example="usuario@correo.com", description="Correo electrónico válido.")
    password: str = Field(None, min_length=8, max_length=255, description="Contraseña de al menos 8 caracteres.")


class ModelUsuario_Google(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Debe contener solo letras y espacios.")
    apellido: str = Field(..., min_length=3, max_length=50, description="Debe contener solo letras y espacios.")
    email: EmailStr = Field(..., example="usuario@correo.com", description="Correo electrónico válido.")
    password: str = Field(None, max_length=255, description="Contraseña de al menos 8 caracteres.")
    google_id: Optional[str] = Field(None, description="Identificador de Google si se registró con Google.")