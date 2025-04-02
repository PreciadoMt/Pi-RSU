from fastapi import  HTTPException,Depends,FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from PDT_Models.ModelUsuario import ModelUsuario
from DB.conexion import Base, engine, Session

app = FastAPI(
    title='FastAPI richy con documentacion',
    description='Ricardo Giovanny Sandoval Bermudez',
    version='0.0.1'
)


#levantar las tabls definidas en los modelo
Base.metadata.create_all(bind=engine)

#Para correr el servidor en la terminal
#.\VEF\Scripts\activate
#uvicorn main:app --reload --port 5000
#Base de datos temporal


@app.get("/",tags=['Raiz'])
def main():
    return {'Hola FastAPI!':' Hola Richy'}

# ---------------Crear un nuevo usuario -----------------------------

@app.get("/Crear_Usuario/", response_model=ModelUsuario,tags=['Usuarios'])
def Crear_u():
    db=Session()
