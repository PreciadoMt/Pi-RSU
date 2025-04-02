# from DB.conexion import Base
# from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean, Enum, Text, TIMESTAMP, Date, Time)
# from sqlalchemy.orm import relationship, declarative_base
# from datetime import datetime
# from sqlalchemy.sql import func

# class Autoevaluacion(Base):
#     __tablename__ = 'autoevaluaciones'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
#     fecha = Column(TIMESTAMP, server_default=func.current_timestamp())
#     puntaje = Column(Integer, nullable=False)
#     interpretacion = Column(Text, nullable=False)
    
#     usuario = relationship("Usuario", back_populates="autoevaluaciones")