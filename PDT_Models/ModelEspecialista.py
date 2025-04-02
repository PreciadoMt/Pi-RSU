from pydantic import BaseModel,Field,EmailStr

class ModelEspecialista(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    apellido: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., example="especialista@correo.com")
    genero: str = Field(..., regex="^(masculino|femenino|otro|prefiero_no_decir)$", description="Debe ser un valor válido.")
    licencia: str = Field(..., min_length=5, max_length=50, description="Número de licencia único.")
    especialidad: str = Field(..., description="Área de especialidad.")
    modelo_terapeutico: Optional[str] = Field(None, description="Enfoque terapéutico.")
    años_experiencia: str = Field(..., regex="^(1-3|4-6|7-10|10\+)$", description="Debe estar en un rango válido.")
    precio: float = Field(..., ge=0, le=10000, description="Precio debe ser un número positivo.")
    verificado: str = Field(True, description="Si el especialista está verificado.")
    foto_perfil: str = Field(None, description="URL de la imagen de perfil.")
    descripcion: str = Field(None, description="Descripción del especialista.")