from fastapi import  HTTPException,Depends,FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from jose import jwt
import httpx
from datetime import datetime, timedelta
from PDT_Models.ModelEspecialista import ModelEspecialista
from PDT_Models.ModelUsuario import ModelUsuario,ModelUsuario_Google
from PDT_Models.ModelLogin import ModelLogin,ModelToken
from DB.conexion import  Session
from DB_Models.DBM_Usuarios import Usuario
from DB_Models.DBM_Especialista import Especialista

SECRET_KEY = 'pswd'
ALGORITHM = 'HS256'

#-------------validar fastapi------------------
app = FastAPI(
    title='Mental Balance FastAPI',
    description='Api de fastapi que enlaza a la base de datos',
    version='0.0.1'
)

@app.get("/",tags=['Raiz'])
def main():
    return {'Hola FastAPI!':' Hola Richy'}

#----------metodos--------------

#crear token para login

def crear_token(email, google_id=None):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": email, "exp": expire}
    if google_id:
        payload["google_id"] = google_id
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ---------------Crear un nuevo usuario -----------------------------
@app.post("/Crear_Usuario/", response_model=ModelUsuario, tags=['Usuarios'])
def Crear_u(usuario_nuevo:ModelUsuario):
    db = Session()
    try:
        
        consulta = db.query(Usuario).filter(Usuario.email == usuario_nuevo.email).first()
        if consulta:
            return JSONResponse(status_code=201,content={"Mensaje":"Correo Ya registrado"})
        
        
        if usuario_nuevo.google_id:  
            consulta2 = db.query(Usuario).filter(Usuario.google_id == usuario_nuevo.google_id).first()
            if consulta2:
                return JSONResponse(status_code=201, content={"Mensaje": "Correo ya registrado, inicia sesion "})
            
        db.add(Usuario(**usuario_nuevo.model_dump()))
        db.commit()
        return JSONResponse(status_code=201,
                             content={
                                 "Mensaje": "Usuario Guardado Correctamente",
                                 "Usuario": usuario_nuevo.model_dump()  
                             })
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,  
                             content={
                                 "Mensaje": "Ha ocurrido un error al Guardar el usuario",
                                 "Excepcion": str(e)
                             })
    finally:
        db.close()
 
# ---------------Crear un nuevo especialista -----------------------------
@app.post("/Crear_Esp/", response_model=ModelEspecialista, tags=['Especialistas'])
def Crear_e(esp_nuevo:ModelEspecialista):
    db = Session()
    try:
      
        existe_email = db.query(Especialista).filter_by(email=esp_nuevo.email).first()
        if existe_email:
            raise HTTPException(status_code=400, detail="Ya existe un especialista con este email")

    
        existe_licencia = db.query(Especialista).filter_by(licencia=esp_nuevo.licencia).first()
        if existe_licencia:
            raise HTTPException(status_code=400, detail="Ya existe un especialista con esta licencia")

    
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
        return JSONResponse(status_code=500,  
                             content={
                                 "Mensaje": "Ha ocurrido un error al Guardar el Especialista",
                                 "Excepcion": str(e)
                             })
    finally:
        db.close()


# ---------------Iniciar sesion-----------------------------
@app.post("/Iniciar_Sesion/",response_model=ModelToken,tags=['Usuarios'])
def Iniciar_s(sesion:ModelLogin):
    db = Session()
    try:
        consulta = db.query(Usuario).filter(Usuario.email == sesion.email).first()
        if consulta:
                if consulta and consulta.password.lower() == sesion.password.lower():
                    token = crear_token(consulta.email)
                    return {'access_token': token, 'token_type': 'bearer'}
                else:
                    return JSONResponse(status_code=401, content={"Mensaje": "Contraseña Incorrecta"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"Mensaje": "Error en el servidor", "Excepcion": str(e)})
    finally:
        db.close()

#---------------------registro con google---------------------
@app.post("/Iniciar_Sesion_Google/", response_model=ModelUsuario_Google, tags=['Usuarios'])
async def Iniciar_s_google(usuario_nuevo: ModelUsuario_Google):
    db = Session()
    try:
        # Buscar al usuario por correo electrónico
        consulta = db.query(Usuario).filter(Usuario.email == usuario_nuevo.email).first()
        
        #codigos de creacion:
        #201 cuando se creo uno nuevo
        #200 cuando el usuario ya esta, simplemente se autentifica#       
         
        if consulta:
            if consulta.google_id != usuario_nuevo.google_id:
                # Realizamos la llamada al endpoint PUT para actualizar el google_id
                async with httpx.AsyncClient() as client:
                    update_url = f"http://127.0.0.1:8000/Actualizar_Google_ID/{usuario_nuevo.email}"
                    response = await client.put(update_url, json=usuario_nuevo.model_dump())
                    
                    if response.status_code == 200:
                        token = crear_token(consulta.email)
                        return JSONResponse(status_code=200, content={  
                            "Mensaje": "Google ID actualizado correctamente",
                            "Usuario": usuario_nuevo.model_dump(),
                            "access_token": token,
                            "token_type": "bearer"
                        })
                    else:
                        #respuesta del put
                        return response  
            else:
                token = crear_token(consulta.email)
                return JSONResponse(status_code=200, content={  
                    "Mensaje": "Usuario autenticado con Google",
                    "Usuario": usuario_nuevo.model_dump(),
                    "access_token": token,
                    "token_type": "bearer"
                })
        else:
            # Si el usuario no existe, lo creamos como nuevo
            db.add(Usuario(**usuario_nuevo.model_dump()))
            db.commit()
            token = crear_token(usuario_nuevo.email)
            return JSONResponse(status_code=201, content={  
                "Mensaje": "Usuario Guardado Correctamente",
                "Usuario": usuario_nuevo.model_dump(),
                "access_token": token,
                "token_type": "bearer"
            })
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={  # Error de servidor
            "Mensaje": "Ha ocurrido un error durante el inicio de sesión con Google",
            "Excepcion": str(e)
        })
    finally:
        db.close()

#---------------------actualizar google id--------------------
#esto es por si un usuario registrado sin google, inicia sesion con google y se le asigna un google id
@app.put("/Actualizar_Google_ID/{email}", response_model=ModelUsuario_Google, tags=['Usuarios'])
def Actualizar_google_id(email:str, usuario_nuevo:ModelUsuario_Google):
    db = Session()
    
    try:
        consulta = db.query(Usuario).filter(Usuario.email == email).first()  
        if consulta:
            consulta.google_id = usuario_nuevo.google_id
            db.commit()
            return JSONResponse(status_code=201, content={"Mensaje": "Google ID actualizado correctamente"})
        else:
            return JSONResponse(status_code=404, content={"Mensaje": "Usuario no encontrado"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"Mensaje": "Error en el servidor", "Excepcion": str(e)})
    finally:
        db.close()

@app.delete("/Eliminar_Usuario/{id}", tags=['Usuarios'])
def Eliminar_usuario(id:int):
    db = Session()
    try:
        consulta = db.query(Usuario).filter(Usuario.id == id).first()
        if consulta:
            db.delete(consulta)
            db.commit()
            return JSONResponse(status_code=200, content={"Mensaje": "Usuario eliminado correctamente"})
        else:
            return JSONResponse(status_code=404, content={"Mensaje": "Usuario no encontrado"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"Mensaje": "Error en el servidor", "Excepcion": str(e)})
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fast:app", host="127.0.0.1", port=9080, reload=True)

