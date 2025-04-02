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


def insertar_especialistas():
    """Inserta datos de prueba en la tabla Especialistas."""
    session = Session()
    try:
        especialistas = [
            Especialista(
                nombre="Juan",
                apellido="Pérez",
                email="juan.perez@example.com",
                genero="masculino",
                licencia="LIC12345",
                especialidad="Psicología clínica",
                modelo_terapeutico="Cognitivo-Conductual",
                años_experiencia="4-6",
                precio=500.00,
                verificado=True,
                foto_perfil=None,
                descripcion="Psicólogo con experiencia en terapia individual."
            ),
            Especialista(
                nombre="María",
                apellido="López",
                email="maria.lopez@example.com",
                genero="femenino",
                licencia="LIC67890",
                especialidad="Psiquiatría",
                modelo_terapeutico="Psicoanalítico",
                años_experiencia="7-10",
                precio=700.00,
                verificado=True,
                foto_perfil=None,
                descripcion="Psiquiatra con enfoque en trastornos de ansiedad."
            )
        ]
        session.add_all(especialistas)
        session.commit()
        print(Fore.GREEN + " Especialistas insertados correctamente." + Fore.RESET)
    except Exception as e:
        session.rollback()
        print(Fore.RED + f" Error al insertar especialistas: {e}" + Fore.RESET)
    finally:
        session.close()


if __name__ == "__main__":
    crear_tablas()
    ver_tablas()
    insertar_especialistas()
    