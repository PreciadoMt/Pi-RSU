from pydantic import BaseModel,Field

class ModelDisponibilidad(BaseModel):
    especialista_id: int = Field(..., gt=0, description="ID del especialista válido.")
    dia: str = Field(..., regex="^(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)$", description="Día de la semana válido.")
    hora_inicio: str = Field(..., regex="^\d{2}:\d{2}:\d{2}$", description="Formato HH:MM:SS")
    hora_fin: str = Field(..., regex="^\d{2}:\d{2}:\d{2}$", description="Formato HH:MM:SS")
    duracion_sesion: int = Field(50, ge=30, le=120, description="Duración en minutos (entre 30 y 120).")
    pausa_entre_sesiones: int = Field(10, ge=0, description="Tiempo de descanso en minutos.")

    @validator("hora_fin")
    def validar_horario(cls, v, values):
        if "hora_inicio" in values:
            if v <= values["hora_inicio"]:
                raise ValueError("La hora de fin debe ser mayor a la de inicio.")
        return v