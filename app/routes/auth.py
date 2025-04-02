from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario, Especialista
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from pathlib import Path

router = APIRouter(prefix="/auth", tags=["Auth"])

# Solo para desarrollo - quitar en producción
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GOOGLE_CLIENT_ID = "943817268512-n52mktn5vi475ajn5qv450cd74kgq4s1.apps.googleusercontent.com"
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", 
            "https://www.googleapis.com/auth/userinfo.email", 
            "openid"],
    redirect_uri="http://127.0.0.1:8090/auth/callback"
)

@router.get("/login/google")
def google_login():
    authorization_url, state = flow.authorization_url()
    return RedirectResponse(url=authorization_url)

@router.get("/callback")
def callback(request: Request, db: Session = Depends(get_db)):
    flow.fetch_token(authorization_response=str(request.url))
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=60
    )
    
    email = id_info.get("email")
    name = id_info.get("name")
    
    user = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not user:
        nombre, apellido = (name.split(' ', 1) + [''])[:2]
        hashed_password = generate_password_hash(os.urandom(24).hex())
        user = Usuario(nombre=nombre, apellido=apellido, email=email, password=hashed_password)
        db.add(user)
        db.commit()
    
    return {"message": f"Bienvenido {user.nombre}", "email": user.email}

@router.post("/registro")
def registro(
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    accept_terms: bool = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")
    
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="Email no válido")
    
    user_exists = db.query(Usuario).filter(Usuario.email == email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Este email ya está registrado")
    
    hashed_password = generate_password_hash(password)
    new_user = Usuario(nombre=nombre, apellido=apellido, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    
    return {"message": "Registro exitoso"}

@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user and check_password_hash(user.password, password):
        return {"message": f"Bienvenido {user.nombre}", "email": user.email}
    
    raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")

@router.get("/logout")
def logout():
    return {"message": "Sesión cerrada"}