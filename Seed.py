from DB.conexion import Base,engine, Session
from DB_Models.DBM_loockups import Roles_Usuarios, Generos, Especialidades, Consultorios, Tipos_Citas, Estatus   # Agrega aquí más modelos conforme los crees
from colorama import Fore, init

init(autoreset=True)  # Configura colorama para resetear colores automáticamente

def insertar_datos():
    """ Inserta datos predeterminados en la base de datos si no existen """
    
    session_db = Session()
    
    # Crear tablas si no existen
    Base.metadata.create_all(engine)

    # 🔹 Inserción de Roles_Usuarios
    if not session_db.query(Roles_Usuarios).first():
        roles = [
            Roles_Usuarios(tipo_usuario="Administrador"),
            Roles_Usuarios(tipo_usuario="Paciente"),
            Roles_Usuarios(tipo_usuario="Psiólogo"),
            
        ]
        session_db.add_all(roles)
        print(Fore.CYAN + "✔ Roles_Usuarios insertados correctamente." + Fore.RESET)
    
    # 🔹 Inserción de Géneros
    if not session_db.query(Generos).first():
        generos = [
            Generos(genero="Masculino"),
            Generos(genero="Femenino"),
            Generos(genero="Otro")
        ]
        session_db.add_all(generos)
        print(Fore.CYAN + "✔ Generos insertados correctamente." + Fore.RESET)
    
    
        
    # 🔹 Inserción de Especialidades
    if not session_db.query(Especialidades).first():
        especialidad = [
            Especialidades(nombre="Vocacion Profesional"),
            Especialidades(nombre="Depresion"),
            Especialidades(nombre="Ansiedad"),
            Especialidades(nombre="Estres"),
            Especialidades(nombre="Autoestima"),
            Especialidades(nombre="Familia"),
            Especialidades(nombre="Pareja"),
            Especialidades(nombre="Sexualidad"),
            Especialidades(nombre="Adicciones"),
            Especialidades(nombre="Trastornos Alimenticios"),
            Especialidades(nombre="Trastornos del Sueño"),
            Especialidades(nombre="Trastornos de Personalidad"),
            Especialidades(nombre="Trastornos Psicoticos"),
            Especialidades(nombre="Trastornos de Ansiedad"),
            Especialidades(nombre="Trastornos del Estado de Animo"),
            Especialidades(nombre="Trastornos de la Conducta"),
            Especialidades(nombre="Trastornos de la Infancia y la Adolescencia"),
            Especialidades(nombre="Trastornos de la Vejez"),
            Especialidades(nombre="Trastornos de la Salud"),
            Especialidades(nombre="Trastornos de la Personalidad"),
            Especialidades(nombre="Trastornos de la Conducta"),
            Especialidades(nombre="Trastornos de la Infancia y la Adolescencia"),
        ]
        session_db.add_all(especialidad)
        print(Fore.CYAN + "✔ Especialidades insertados correctamente." + Fore.RESET)

    # 🔹 Inserción de Consultorios
    if not session_db.query(Consultorios).first():
        consultorio = [
            Consultorios(nombre="Consultorio 1"),
            Consultorios(nombre="Consultorio 2"),
            Consultorios(nombre="Consultorio 3"),
            Consultorios(nombre="Consultorio 4"),
            Consultorios(nombre="Consultorio 5"),
            Consultorios(nombre="Consultorio 6"),
            Consultorios(nombre="Consultorio 7"),
            Consultorios(nombre="Consultorio 8"),
            Consultorios(nombre="Consultorio 9"),
            Consultorios(nombre="Consultorio 10"),
        ]
        session_db.add_all(consultorio)
        print(Fore.CYAN + "✔ Consultorios insertados correctamente." + Fore.RESET)
    
    # 🔹 Inserción de Tipos_Citas
    if not session_db.query(Tipos_Citas).first():
        cita = [
            Tipos_Citas(nombre="Presencial"),
            Tipos_Citas(nombre="Virtual"),
            Tipos_Citas(nombre="Telefonica"),
            Tipos_Citas(nombre="Chat"),
            Tipos_Citas(nombre="VideoLlamada"),
        ]
        session_db.add_all(cita)
        print(Fore.CYAN + "✔ Tipos_Citas insertados correctamente." + Fore.RESET)
    
    # 🔹 Inserción de Estatus
    if not session_db.query(Estatus).first():
        estatus = [
            Estatus(nombre="Activo"),
            Estatus(nombre="Inactivo"),
            Estatus(nombre="Pendiente"),
            Estatus(nombre="Cancelado"),
            Estatus(nombre="Finalizado"),
            Estatus(nombre="En Proceso"),
        ]
        session_db.add_all(estatus)
        print(Fore.CYAN + "✔ Estatus insertados correctamente." + Fore.RESET)
    
    
    
    session_db.commit()
    print(Fore.GREEN + "✔Datos insertados correctamente." + Fore.RESET)
    
    session_db.close()

if __name__ == "__main__":
    insertar_datos()
