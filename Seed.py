from DB.conexion import Base, engine, Session
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from colorama import Fore, init
from DB_Models import DBM_Citas, DBM_Disponibilidad, DBM_Especialista, DBM_Evaluaciones, DBM_Recomendaciones, DBM_Usuarios
from DB_Models.DBM_Especialista import Especialista
from DB_Models.DBM_Usuarios import Usuario


init(autoreset=True)  # Configura colorama para resetear colores automáticamente

def crear_tablas():
    """Crea todas las tablas en la base de datos."""
    Base.metadata.create_all(engine)
    print(Fore.GREEN + " Tablas creadas correctamente." + Fore.RESET)


def ver_tablas():
    """Muestra las tablas de la base de datos."""
    inspector = inspect(engine)  # Inspeccionar la base de datos a través del engine
    tablas = inspector.get_table_names()  # Obtener los nombres de las tablas
    print(Fore.CYAN + "Tablas en la base de datos:" + Fore.RESET)
    for tabla in tablas:
        print(Fore.YELLOW + tabla + Fore.RESET)


def insertar_admin(nombre, apellido, email, password, google_id=None):
    """Inserta un nuevo usuario en la base de datos."""
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=password,  # Asegúrate de hashear la contraseña en producción
            google_id=google_id
        )

        # Añadir el nuevo usuario a la sesión
        session.add(nuevo_usuario)
        
        # Hacer commit para guardar el usuario en la base de datos
        session.commit()
        print("Usuario insertado correctamente.")

    except Exception as e:
        session.rollback()
        print(f"Error al insertar el usuario: {str(e)}")
    
    finally:
        session.close()

if __name__ == "__main__":
    crear_tablas()
    ver_tablas()
    insertar_admin("Ricardo", "Sandoval", "admin@mentalbalance.com", "ADMIN12345")
    