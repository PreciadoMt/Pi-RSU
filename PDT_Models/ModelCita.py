from pydantic import BaseModel,Field

class ModelCita(BaseModel):
    usuario_id: int = Field(..., gt=0, description="ID de usuario válido.")
    especialista_id: int = Field(..., gt=0, description="ID de especialista válido.")
    fecha: str = Field(..., regex="^\d{4}-\d{2}-\d{2}$", description="Formato YYYY-MM-DD.")
    hora_inicio: str = Field(..., regex="^\d{2}:\d{2}:\d{2}$", description="Formato HH:MM:SS.")
    hora_fin: str = Field(..., regex="^\d{2}:\d{2}:\d{2}$", description="Formato HH:MM:SS.")
    motivo_consulta: Optional[str] = Field(None, description="Motivo de la consulta.")
    estado: str = Field("pendiente", regex="^(pendiente|confirmada|completada|cancelada|rechazada)$", description="Estado de la cita.")
    notas: str = Field(None, description="Notas adicionales.")