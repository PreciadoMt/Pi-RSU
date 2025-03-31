#nota: para un proyecto es recomendado tener un archivo por cada modelo
# es decir, un archivo de models por tabla para ubicarlas mas facilmente
#atributos de las tablas en minusculas, nombres de las tablas empezar por mayuscula y en plural
#ademas el nombre de la tabla dentro de la clase empezara con "tb_<nombre de la tabla>"

from DB.conexion import Base
from sqlalchemy import Column,Integer,String,ForeignKey  

class Usuarios(Base):
    __tablename__='tb_Usuarios'
    id_usuario=Column(Integer,primary_key=True,autoincrement='auto')
    nombre=Column(String)
    apellido=Column(String)
    correo_electronico=Column(String)
    contrasena=Column(String)
    telefono=Column(String)
    id_tipo_usuario = Column(Integer, ForeignKey('tb_Roles_Usuarios.id_rol'))
    id_genero = Column(Integer, ForeignKey('tb_Generos.id_genero'))

