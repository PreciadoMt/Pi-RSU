from fastapi import  HTTPException,Depends,FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from PDT_Models.ModelEspecialista import ModelEspecialista
from PDT_Models.ModelUsuario import ModelUsuario
from DB.conexion import Base, engine, Session
from DB_Models.DBM_Usuarios import Usuario
from DB_Models.DBM_Especialista import Especialista

app = FastAPI(
    title='Mental Balance FastAPI',
    description='Api de fastapi que enlaza a la base de datos',
    version='0.0.1'
)

@app.get("/",tags=['Raiz'])
def main():
    return {'Hola FastAPI!':' Hola Richy'}

# ---------------Crear un nuevo usuario -----------------------------
@app.post("/Crear_Usuario/", response_model=ModelUsuario, tags=['Usuarios'])
def Crear_u(usuario_nuevo:ModelUsuario):
    db = Session()
    try:
        db.add(Usuario(**usuario_nuevo.model_dump()))
        db.commit()
        return JSONResponse(status_code=201,
                             content={
                                 "Mensaje": "Usuario Guardado Correctamente",
                                 "Usuario": usuario_nuevo.model_dump()  # Deberías devolver el mismo usuario que creaste
                             })
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,  # Código de error interno
                             content={
                                 "Mensaje": "Ha ocurrido un error al Guardar el usuario",
                                 "Excepcion": str(e)
                             })
    finally:
        db.close()
# ---------------Crear un nuevo especialista -----------------------------
@app.post("/Crear_Esp/", response_model=ModelEspecialista, tags=['Especialista'])
def Crear_e(esp_nuevo:ModelEspecialista):
    db = Session()
    try:
         # Verificar si el especialista ya existe por email
        existe_email = db.query(Especialista).filter_by(email=esp_nuevo.email).first()
        if existe_email:
            raise HTTPException(status_code=400, detail="Ya existe un especialista con este email")

        # Verificar si el especialista ya existe por licencia
        existe_licencia = db.query(Especialista).filter_by(licencia=esp_nuevo.licencia).first()
        if existe_licencia:
            raise HTTPException(status_code=400, detail="Ya existe un especialista con esta licencia")

        # Si no existe, lo creamos
        nuevo_especialista = Especialista(**esp_nuevo.model_dump())
        db.add(nuevo_especialista)
        db.commit()
        db.refresh(nuevo_especialista)

        return JSONResponse(
            status_code=201,
            content={
                "Mensaje": "Especialista Guardado Correctamente",
                "Usuario": esp_nuevo.model_dump()
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,  # Código de error interno
                             content={
                                 "Mensaje": "Ha ocurrido un error al Guardar el Especialista",
                                 "Excepcion": str(e)
                             })
    finally:
        db.close()

@app.get("/generar_horarios_disponibles/", response_model=ModelUsuario,tags=['Usuarios'])
def Crear_u():
    db=Session()
  
