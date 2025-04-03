from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum

# Enum para especialidad
class EspecialidadEnum(str, Enum):
    psicologia_clinica = 'Psicología clínica'
    psiquiatria = 'Psiquiatría'
    terapia_cognitivo_conductual = 'Terapia cognitivo-conductual'
    psicoanalisis = 'Psicoanálisis'
    terapia_familiar = 'Terapia familiar'
    terapia_de_pareja = 'Terapia de pareja'
    neuropsicologia = 'Neuropsicología'
    psicologia_infantil = 'Psicología infantil'
    psicologia_educativa = 'Psicología educativa'
    psicologia_organizacional = 'Psicología organizacional'
    otra = 'Otra'

# Enum para modelo terapéutico
class ModeloTerapeuticoEnum(str, Enum):
    cognitivo_conductual = 'Cognitivo-Conductual'
    psicoanalitico = 'Psicoanalítico'
    humanista = 'Humanista'
    sistemico = 'Sistémico'
    integrativo = 'Integrativo'
    otro = 'Otro'

# Enum para años de experiencia
class AnosExperienciaEnum(str, Enum):
    uno_a_tres = '1-3'
    cuatro_a_seis = '4-6'
    siete_a_diez = '7-10'
    diez_mas = '10+'

# Modelo Pydantic para el especialista
class ModelEspecialista(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    apellido: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., example="especialista@correo.com")
    genero: str = Field(..., pattern="^(masculino|femenino|otro|prefiero_no_decir)$", description="Debe ser un valor válido.")
    licencia: str = Field(..., min_length=5, max_length=50, description="Número de licencia único.")
    password: str = Field(..., min_length=8, max_length=16)
    especialidad: EspecialidadEnum
    modelo_terapeutico: Optional[ModeloTerapeuticoEnum] = Field(None, description="Enfoque terapéutico.")
    años_experiencia: AnosExperienciaEnum
    precio: Optional[float] = Field(None, ge=0, le=10000, description="Precio debe ser un número positivo.")
    verificado: Optional[bool] = Field(default=True, description="Indica si el especialista está verificado")
    foto_perfil: Optional[str] = Field(None, description="URL de la imagen de perfil.")
    descripcion: Optional[str] = Field(None, description="Descripción del especialista.")

    class Config:
        use_enum_values = True
