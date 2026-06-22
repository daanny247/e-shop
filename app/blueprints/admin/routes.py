from flask import render_template
from . import auth_bp

@admin_bp.route('/admin')
def login():
    return render_template('admin/login.html')

@admin_bp.route('/admin/productos')
def registro():
    return render_template('admin/registro.html')

@admin_bp.route('/admin/clientes')
def login():
    return render_template('admin/login.html')

@admin_bp.route('/admin/pedidos')
def registro():
    return render_template('admin/registro.html')
    