from DB.conexion import Base
from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean, Enum, Text, TIMESTAMP, Date, Time)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime


class Cita(Base):
    __tablename__ = 'citas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    especialista_id = Column(Integer, ForeignKey('especialistas.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    motivo_consulta = Column(Text, nullable=True)
    estado = Column(Enum('pendiente', 'confirmada', 'completada', 'cancelada', 'rechazada'), default='pendiente')
    notas = Column(Text, nullable=True)
    creada_en = Column(TIMESTAMP, default=datetime.utcnow)
    actualizada_en = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="citas")
    especialista = relationship("Especialista", back_populates="citas")