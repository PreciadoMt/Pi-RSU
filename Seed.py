from DB.conexion import Base, engine, Session
from sqlalchemy import inspect
from colorama import Fore, init
from DB_Models import DBM_Citas, DBM_Disponibilidad, DBM_Especialista, DBM_Evaluaciones, DBM_Recomendaciones, DBM_Usuarios
from DB_Models.DBM_Especialista import Especialista



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


if __name__ == "__main__":
    crear_tablas()
    ver_tablas()

    