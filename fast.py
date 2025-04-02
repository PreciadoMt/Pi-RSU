from fastapi import  HTTPException,Depends,FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from PDT_Models.ModelUsuario import ModelUsuario
from DB.conexion import Base, engine, Session
from DB_Models.DBM_Usuarios import Usuario

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
        
@app.get("/generar_horarios_disponibles/", response_model=ModelUsuario,tags=['Usuarios'])
def Crear_u():
    db=Session()
  
