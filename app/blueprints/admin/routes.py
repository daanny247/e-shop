from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Categoria, Producto, Usuario, Pedido
from . import admin_bp
from .decorators import admin_requerido
from .forms import CategoriaForm, ProductoForm
from .utils import guardar_imagen_producto, eliminar_imagen_producto

UMBRAL_STOCK_BAJO = 5
ESTADOS_PEDIDO = ['pendiente', 'pagado', 'enviado', 'entregado', 'cancelado']


@admin_bp.before_request
@login_required
@admin_requerido
def proteger_admin():
    """Todas las rutas del panel requieren sesión activa y rol de administrador."""
    pass


def _cargar_opciones_categoria(form):
    form.categoria_id.choices = [
        (c.id, c.nombre) for c in Categoria.query.order_by(Categoria.nombre).all()
    ]


# ── DASHBOARD ─────────────────────────────────────────────────────
@admin_bp.route('/dashboard')
def dashboard():
    ventas_total = db.session.query(
        func.coalesce(func.sum(Pedido.total), 0)
    ).filter(Pedido.estado != 'cancelado').scalar()

    pedidos_total = Pedido.query.count()
    pedidos_pendientes = Pedido.query.filter_by(estado='pendiente').count()

    productos_bajo_stock = Producto.query.filter(
        Producto.activo == True,
        Producto.stock <= UMBRAL_STOCK_BAJO
    ).order_by(Producto.stock.asc()).all()

    return render_template('admin/dashboard.html',
                           ventas_total=ventas_total,
                           pedidos_total=pedidos_total,
                           pedidos_pendientes=pedidos_pendientes,
                           productos_bajo_stock=productos_bajo_stock,
                           umbral_stock=UMBRAL_STOCK_BAJO)


# ── CATEGORÍAS ────────────────────────────────────────────────────
@admin_bp.route('/categorias')
def categorias():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template('admin/categorias_list.html', categorias=categorias)


@admin_bp.route('/categorias/nueva', methods=['GET', 'POST'])
def categoria_nueva():
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria = Categoria(nombre=form.nombre.data, descripcion=form.descripcion.data)
        db.session.add(categoria)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Ya existe una categoría con ese nombre.', 'danger')
            return render_template('admin/categoria_form.html', form=form, titulo='Nueva categoría')

        flash(f'Categoría "{categoria.nombre}" creada.', 'success')
        return redirect(url_for('admin.categorias'))

    return render_template('admin/categoria_form.html', form=form, titulo='Nueva categoría')


@admin_bp.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
def categoria_editar(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm(obj=categoria)

    if form.validate_on_submit():
        categoria.nombre = form.nombre.data
        categoria.descripcion = form.descripcion.data
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Ya existe una categoría con ese nombre.', 'danger')
            return render_template('admin/categoria_form.html', form=form, titulo='Editar categoría')

        flash(f'Categoría "{categoria.nombre}" actualizada.', 'success')
        return redirect(url_for('admin.categorias'))

    return render_template('admin/categoria_form.html', form=form, titulo='Editar categoría')


@admin_bp.route('/categorias/<int:id>/eliminar', methods=['POST'])
def categoria_eliminar(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.activa = not categoria.activa
    db.session.commit()
    estado = 'activada' if categoria.activa else 'desactivada'
    flash(f'Categoría "{categoria.nombre}" {estado}.', 'info')
    return redirect(url_for('admin.categorias'))


# ── PRODUCTOS ─────────────────────────────────────────────────────
@admin_bp.route('/productos')
def productos():
    categoria_id = request.args.get('categoria', type=int)

    query = Producto.query
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    productos = query.order_by(Producto.nombre).all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()

    return render_template('admin/productos_list.html',
                           productos=productos, categorias=categorias,
                           categoria_id=categoria_id)


@admin_bp.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    form = ProductoForm()
    _cargar_opciones_categoria(form)

    if form.validate_on_submit():
        producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            stock=form.stock.data,
            categoria_id=form.categoria_id.data,
            imagen=guardar_imagen_producto(form.imagen.data)
        )
        db.session.add(producto)
        db.session.commit()
        flash(f'Producto "{producto.nombre}" creado.', 'success')
        return redirect(url_for('admin.productos'))

    return render_template('admin/producto_form.html', form=form, titulo='Nuevo producto', producto=None)


@admin_bp.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
def producto_editar(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm()
    _cargar_opciones_categoria(form)

    if request.method == 'GET':
        form.nombre.data = producto.nombre
        form.descripcion.data = producto.descripcion
        form.precio.data = producto.precio
        form.stock.data = producto.stock
        form.categoria_id.data = producto.categoria_id

    if form.validate_on_submit():
        nueva_imagen = guardar_imagen_producto(form.imagen.data)
        if nueva_imagen:
            eliminar_imagen_producto(producto.imagen)
            producto.imagen = nueva_imagen

        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.precio = form.precio.data
        producto.stock = form.stock.data
        producto.categoria_id = form.categoria_id.data
        db.session.commit()
        flash(f'Producto "{producto.nombre}" actualizado.', 'success')
        return redirect(url_for('admin.productos'))

    return render_template('admin/producto_form.html', form=form, titulo='Editar producto', producto=producto)


@admin_bp.route('/productos/<int:id>/eliminar', methods=['POST'])
def producto_eliminar(id):
    producto = Producto.query.get_or_404(id)
    producto.activo = not producto.activo
    db.session.commit()
    estado = 'activado' if producto.activo else 'desactivado'
    flash(f'Producto "{producto.nombre}" {estado}.', 'info')
    return redirect(url_for('admin.productos'))


# ── CLIENTES ──────────────────────────────────────────────────────
@admin_bp.route('/clientes')
def clientes():
    clientes = Usuario.query.filter_by(rol='cliente').order_by(Usuario.nombre).all()
    return render_template('admin/clientes_list.html', clientes=clientes)


@admin_bp.route('/clientes/<int:id>/toggle', methods=['POST'])
def cliente_toggle(id):
    cliente = Usuario.query.get_or_404(id)

    if cliente.rol == 'admin':
        flash('No se puede desactivar una cuenta de administrador.', 'warning')
        return redirect(url_for('admin.clientes'))

    cliente.activo = not cliente.activo
    db.session.commit()
    estado = 'activada' if cliente.activo else 'desactivada'
    flash(f'Cuenta de "{cliente.nombre}" {estado}.', 'info')
    return redirect(url_for('admin.clientes'))


# ── PEDIDOS ───────────────────────────────────────────────────────
@admin_bp.route('/pedidos')
def pedidos():
    estado_filtro = request.args.get('estado', '')

    query = Pedido.query
    if estado_filtro:
        query = query.filter_by(estado=estado_filtro)

    pedidos = query.order_by(Pedido.fecha.desc()).all()

    return render_template('admin/pedidos_list.html',
                           pedidos=pedidos, estados=ESTADOS_PEDIDO,
                           estado_filtro=estado_filtro)


@admin_bp.route('/pedidos/<int:id>/estado', methods=['POST'])
def pedido_cambiar_estado(id):
    pedido = Pedido.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')

    if nuevo_estado not in ESTADOS_PEDIDO:
        flash('Estado inválido.', 'danger')
        return redirect(url_for('admin.pedidos'))

    pedido.estado = nuevo_estado
    db.session.commit()
    flash(f'Pedido #{pedido.id} actualizado a "{nuevo_estado}".', 'success')
    return redirect(url_for('admin.pedidos'))
