from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql
import re
import os
import json
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from pathlib import Path

auth_bp = Blueprint('auth', __name__)

# Solo para desarrollo - quitar en producción
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
google_client_id = "943817268512-n52mktn5vi475ajn5qv450cd74kgq4s1.apps.googleusercontent.com"
client_secrets_file = os.path.join(BASE_DIR, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", 
            "https://www.googleapis.com/auth/userinfo.email", 
            "openid"],
    redirect_uri="http://127.0.0.1:8090/callback"
)

@auth_bp.route('/login/google')
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@auth_bp.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session.get("state") == request.args.get("state"):
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_client_id,
        clock_skew_in_seconds=60
    )
    
    email = id_info.get("email")
    name = id_info.get("name")
    
    try:
        
        cur = mysql.connection.cursor()
        
        # Verificar si el usuario ya existe
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if not user:
            # Dividir el nombre en nombre y apellido
            nombre, apellido = (name.split(' ', 1) + [''])[:2]  # Asegura que siempre haya 2 elementos
            
            # Crear nuevo usuario con contraseña aleatoria
            cur.execute(
                "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)",
                (nombre, apellido, email, generate_password_hash(os.urandom(24).hex()))
            )
            mysql.connection.commit()
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cur.fetchone()
        
        # Configurar sesión
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        session['user_name'] = f"{user['nombre']} {user['apellido']}"
        session['user_type'] = 'usuario'
        flash(f'¡Bienvenido/a {user["nombre"]}! Has iniciado sesión con Google', 'success')
        
        return redirect(url_for('general.inicio'))
    
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error durante el login con Google: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['first_name'].strip()
        apellido = request.form['last_name'].strip()
        email = request.form['email'].lower().strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        accept_terms = request.form.get('accept_terms') == 'on'

        # Validaciones
        if not all([nombre, apellido, email, password, confirm_password]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('auth.registro'))

        if not accept_terms:
            flash('Debes aceptar los términos y condiciones', 'danger')
            return redirect(url_for('auth.registro'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.registro'))

        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'danger')
            return redirect(url_for('auth.registro'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Email no válido', 'danger')
            return redirect(url_for('auth.registro'))

        try:
            # Verificar si el email ya existe
            cur = mysql.connection.cursor()
            cur.execute("SELECT email FROM usuarios WHERE email = %s UNION SELECT email FROM especialistas WHERE email = %s", (email, email))
            if cur.fetchone():
                flash('Este email ya está registrado', 'danger')
                return redirect(url_for('auth.registro'))

            # Insertar nuevo usuario
            hashed_pw = generate_password_hash(password)
            cur.execute(
                "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)",
                (nombre, apellido, email, hashed_pw)
            )
            mysql.connection.commit()
            cur.close()

            flash('¡Registro exitoso! Por favor inicia sesión', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            mysql.connection.rollback()
            flash('Error en el servidor: ' + str(e), 'danger')

    return render_template('auth/registro.html')

@auth_bp.route('/registroEspecialista', methods=['GET', 'POST'])
def registro_especialista():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['first_name'].strip()
        apellido = request.form['last_name'].strip()
        email = request.form['email'].lower().strip()
        genero = request.form['gender']
        licencia = request.form['license'].strip()
        especialidad = request.form['specialization']
        años_experiencia = request.form['experience']
        password = request.form['password']
        precio = int(request.form['precio'])
        confirm_password = request.form['confirm_password']
        accept_terms = request.form.get('accept_terms') == 'on'

        # Validaciones
        if not all([nombre, apellido, email, genero, licencia, especialidad, años_experiencia, password, confirm_password]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('auth.registro_especialista'))

        if not accept_terms:
            flash('Debes aceptar el código de ética profesional', 'danger')
            return redirect(url_for('auth.registro_especialista'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.registro_especialista'))

        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'danger')
            return redirect(url_for('auth.registro_especialista'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Email no válido', 'danger')
            return redirect(url_for('auth.registro_especialista'))

        # Crear diccionario JSON
        especialista_data = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "genero": genero,
            "licencia": licencia,
            "especialidad": especialidad,
            "años_experiencia": años_experiencia,
            "precio": precio
        }

        
        especialista_json = json.dumps(especialista_data)
        print(especialista_json)
        # Enviar datos a FastAPI
        try:
            url = "http://127.0.0.1:9080/Crear_Esp/"  # Reemplázalo con la URL de tu API
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=especialista_json, headers=headers)

            if response.status_code == 200:
                flash('Registro exitoso', 'success')
            else:
                flash(f'Error en la API: {response.text}', 'danger')

        except requests.exceptions.RequestException as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')

    return render_template('auth/registroEspecialista.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username'].lower().strip()
        password = request.form['password']

        try:
            cur = mysql.connection.cursor()
            
            # Primero buscar en usuarios
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cur.fetchone()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_name'] = f"{user['nombre']} {user['apellido']}"
                session['user_type'] = 'usuario'
                flash(f'¡Bienvenido/a {user["nombre"]}!', 'success')
                return redirect(url_for('general.inicio'))
            
            # Si no es usuario, buscar en especialistas
            cur.execute("SELECT * FROM especialistas WHERE email = %s", (email,))
            especialista = cur.fetchone()
            
            if especialista:
                if check_password_hash(especialista['password'], password):
                    if not especialista['verificado']:
                        flash('Tu cuenta aún no ha sido verificada. Por favor espera la confirmación.', 'warning')
                        return redirect(url_for('auth.login'))
                    
                    session['user_id'] = especialista['id']
                    session['user_email'] = especialista['email']
                    session['user_name'] = f"{especialista['nombre']} {especialista['apellido']}"
                    session['user_type'] = 'especialista'
                    flash(f'¡Bienvenido/a profesional {especialista["nombre"]}!', 'success')
                    return redirect(url_for('general.inicio'))
                else:
                    flash('Email o contraseña incorrectos', 'danger')
            else:
                flash('Email o contraseña incorrectos', 'danger')

            cur.close()

        except Exception as e:
            flash('Error en el servidor: ' + str(e), 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('general.inicio'))