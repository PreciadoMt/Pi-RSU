from DB.conexion import Base
from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean, Enum, Text, TIMESTAMP, Date, Time)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from sqlalchemy.sql import func

class Recomendacion(Base):
    __tablename__ = 'recomendaciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    especialista_id = Column(Integer, ForeignKey('especialistas.id'), nullable=False)
    mensaje = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    usuario = relationship("Usuario", back_populates="recomendaciones")
    especialista = relationship("Especialista", back_populates="recomendaciones")