#nota: para un proyecto es recomendado tener un archivo por cada modelo
# es decir, un archivo de models por tabla para ubicarlas mas facilmente
#atributos de las tablas en minusculas, nombres de las tablas empezar por mayuscula y en plural
#ademas el nombre de la tabla dentro de la clase empezara con "tb_<nombre de la tabla>"

from DB.conexion import Base
from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean, Enum, Text, TIMESTAMP, Date, Time)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    google_id = Column(String(255), unique=True, nullable=True)
    creado_en = Column(TIMESTAMP, default=datetime.utcnow)
    
    citas = relationship("Cita", back_populates="usuario")
    # autoevaluaciones = relationship('Autoevaluacion', back_populates='usuario')
