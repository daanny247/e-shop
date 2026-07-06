from flask import render_template
from . import admin_bp
from flask_login import login_required
from .decorators import admin_requerido

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/home.html')

@admin_bp.route('/admin/productos')
def registro():
    return render_template('admin/registro.html')

@admin_bp.route('/admin/clientes')
def clientes():
    return render_template('admin/login.html')

@admin_bp.route('/admin/pedidos')
def pedidos():
    return render_template('admin/pedidos.html')
    