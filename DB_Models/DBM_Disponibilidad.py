#nota: para un proyecto es recomendado tener un archivo por cada modelo
# es decir, un archivo de models por tabla para ubicarlas mas facilmente
#atributos de las tablas en minusculas, nombres de las tablas empezar por mayuscula y en plural
#ademas el nombre de la tabla dentro de la clase empezara con "tb_<nombre de la tabla>"
from DB.conexion import Base
from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean, Enum, Text, TIMESTAMP, Date, Time)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

class Disponibilidad(Base):
    __tablename__ = 'disponibilidad'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    especialista_id = Column(Integer, ForeignKey('especialistas.id'), nullable=False)
    dia = Column(Enum('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    duracion_sesion = Column(Integer, nullable=False, default=50)
    pausa_entre_sesiones = Column(Integer, nullable=False, default=10)
    
    especialista = relationship("Especialista", back_populates="disponibilidad")

    