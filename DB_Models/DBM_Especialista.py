#nota: para un proyecto es recomendado tener un archivo por cada modelo
# es decir, un archivo de models por tabla para ubicarlas mas facilmente
#atributos de las tablas en minusculas, nombres de las tablas empezar por mayuscula y en plural
#ademas el nombre de la tabla dentro de la clase empezara con "tb_<nombre de la tabla>"
from DB.conexion import Base
from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean, Enum, Text, TIMESTAMP, Date, Time)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

class Especialista(Base):
    __tablename__ = 'especialistas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    genero = Column(Enum('masculino', 'femenino', 'otro', 'prefiero_no_decir'), nullable=False)
    licencia = Column(String(50), unique=True, nullable=False)
    password = Column(String(8))
    especialidad = Column(Enum(
        'Psicología clínica', 'Psiquiatría', 'Terapia cognitivo-conductual', 'Psicoanálisis',
        'Terapia familiar', 'Terapia de pareja', 'Neuropsicología', 'Psicología infantil',
        'Psicología educativa', 'Psicología organizacional', 'Otra'
    ), nullable=False)
    modelo_terapeutico = Column(Enum('Cognitivo-Conductual', 'Psicoanalítico', 'Humanista', 'Sistémico', 'Integrativo', 'Otro'), nullable=True)
    años_experiencia = Column(Enum('1-3', '4-6', '7-10', '10+'), nullable=False)
    precio = Column(DECIMAL(8, 2), nullable=False, default=400.00)
    verificado = Column(Boolean, default=True)
    creado_en = Column(TIMESTAMP, default=datetime.utcnow)
    foto_perfil = Column(String(255), nullable=True)
    descripcion = Column(Text, nullable=True)
    
    disponibilidad = relationship("Disponibilidad", back_populates="especialista")
    citas = relationship("Cita", back_populates="especialista")