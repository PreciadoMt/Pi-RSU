#nota: para un proyecto es recomendado tener un archivo por cada modelo
# es decir, un archivo de models por tabla para ubicarlas mas facilmente
#atributos de las tablas en minusculas, nombres de las tablas empezar por mayuscula y en plural
#ademas el nombre de la tabla dentro de la clase empezara con "tb_<nombre de la tabla>"
from DB.conexion import Base
from sqlalchemy import Column,Integer,String,ForeignKey  

class Roles_Usuarios(Base):
    __tablename__='tb_Roles_Usuarios'
    id_rol=Column(Integer,primary_key=True,autoincrement='auto')
    tipo_usuario=Column(String)

class Generos(Base):
    __tablename__='tb_Generos'
    id_genero=Column(Integer,primary_key=True,autoincrement='auto')
    genero=Column(String)
    

class Especialidades(Base):
    __tablename__='tb_Especialidades'
    id_especialidades=Column(Integer,primary_key=True,autoincrement='auto')
    nombre=Column(String)
    
class Consultorios(Base):
    __tablename__='tb_Consultorios'
    id_Consultorio=Column(Integer,primary_key=True,autoincrement='auto')
    nombre=Column(String)

class Tipos_Citas(Base):
    __tablename__='tb_Tipos_Citas'
    id_tipo_cita=Column(Integer,primary_key=True,autoincrement='auto')
    nombre=Column(String)

class Estatus(Base):
    __tablename__='tb_Estatus'
    id_estatus=Column(Integer,primary_key=True,autoincrement='auto')
    nombre=Column(String)
      