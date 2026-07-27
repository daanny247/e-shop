from app import create_app, db
from app.models import Usuario, Categoria, Producto

app = create_app()

with app.app_context():
    if Categoria.query.first() is not None:
        print("La base de datos ya tiene categorías cargadas; no se vuelve a sembrar.")
        print("Si quieres datos limpios, vacía las tablas primero.")
        raise SystemExit(0)

    # Categorías
    cat_hombre  = Categoria(nombre='Hombre',  descripcion='Fragancias masculinas')
    cat_mujer   = Categoria(nombre='Mujer',   descripcion='Fragancias femeninas')
    cat_unisex  = Categoria(nombre='Unisex',  descripcion='Fragancias para todos')
    db.session.add_all([cat_hombre, cat_mujer, cat_unisex])
    db.session.commit()

    # Productos
    productos = [
        # Hombre
        Producto(
            nombre='Noir Intense', 
            descripcion='Eau de parfum amaderada con notas de cuero y vetiver.',
            precio=54.99, 
            stock=25, 
            categoria_id=cat_hombre.id,
            imagen='noir-intense.jpg'
        ),
        Producto(
            nombre='Velvet Oud', 
            descripcion='Fragancia intensa con oud, especias y toques ahumados.',
            precio=69.90, 
            stock=15, 
            categoria_id=cat_hombre.id,
            imagen='velvet-oud.jpg'
        ),
        Producto(
            nombre='Acero Nocturno', 
            descripcion='Notas frescas de bergamota y un fondo especiado.',
            precio=42.50, 
            stock=30, 
            categoria_id=cat_hombre.id,
            imagen='acero-nocturno.jpg'
        ),

        # Mujer
        Producto(
            nombre='Rosa Blanca', 
            descripcion='Eau de parfum floral con rosa blanca y almizcle suave.',
            precio=59.99, 
            stock=20, 
            categoria_id=cat_mujer.id,
            imagen='rosa-blanca.jpg'
        ),
        Producto(
            nombre='Jazmín Dorado', 
            descripcion='Notas de jazmín, vainilla y un toque de sándalo.',
            precio=64.50, 
            stock=18, 
            categoria_id=cat_mujer.id,
            imagen='jazmin-dorado.jpg'
        ),
        Producto(
            nombre='Dulce Peonía', 
            descripcion='Fragancia luminosa de peonía, frutos rojos y almizcle.',
            precio=47.00, 
            stock=22, 
            categoria_id=cat_mujer.id,
            imagen='dulce-peonia.jpg'
        ),

        # Unisex
        Producto(
            nombre='Brisa Marina', 
            descripcion='Fragancia unisex acuática con notas cítricas.',
            precio=39.99, 
            stock=35, 
            categoria_id=cat_unisex.id,
            imagen='brisa-marina.jpg'
        ),
        Producto(
            nombre='Ámbar Místico', 
            descripcion='Ámbar, sándalo y vainilla en una fragancia unisex envolvente.',
            precio=57.90, 
            stock=12, 
            categoria_id=cat_unisex.id,
            imagen='ambar-mistico.jpg'
        ),
    ]
    db.session.add_all(productos)

    # Usuarios
    admin = Usuario(nombre='Administrador', email='admin@scenthub.com', rol='admin')
    admin.set_password('admin123')

    cliente = Usuario(nombre='Juan Pérez', email='juan@email.com', rol='cliente')
    cliente.set_password('cliente123')

    db.session.add_all([admin, cliente])
    db.session.commit()

    print("Datos de ScentHub insertados correctamente")