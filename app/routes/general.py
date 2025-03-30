from flask import Blueprint, render_template, flash

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
