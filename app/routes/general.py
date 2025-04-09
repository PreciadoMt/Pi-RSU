from flask import Blueprint, render_template, flash
from .auth import token_required

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def inicio():
    return render_template('general/inicio.html')

@general_bp.route('/depresion')
def depresion():
    return render_template('depresion.html') 

@general_bp.route('/ansiedad')
def ansiedad():
    return render_template('general/ansiedad.html')

@general_bp.route('/familia')
def familia():
    return render_template('general/familia.html') 

@general_bp.route('/nosotros')
def nosotros():
    return render_template('general/nosotros.html') 

@general_bp.route('/profesionales')
@token_required
def profesionales():
    return render_template('general/profesionales.html') 


@general_bp.route('/test')
@token_required
def test():
    return render_template('general/test.html') 


@general_bp.route('/prediagnnostico')
def prediagnostico():
    return render_template('general/prediagnostico.html') 