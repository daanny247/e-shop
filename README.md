# ScentHub

Tienda en línea de perfumería desarrollada con Flask. Incluye catálogo de
productos, carrito de compras, autenticación de usuarios, seguimiento de
pedidos y un panel de administración completo (categorías, productos,
clientes y pedidos).

**Equipo:** Nicolás Zambrano Rivera, José Rafael Catucuamba Ulcuango,
Danny Alexander Peñaherrera Cárdenas

## Requisitos

- Python 3.11+
- MySQL 8+ (o compatible)

## Instalación (desarrollo local)

1. Clonar el repositorio y entrar a la carpeta del proyecto.

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   ```

   Windows (PowerShell):
   ```bash
   .venv\Scripts\Activate.ps1
   ```

   Linux / macOS:
   ```bash
   source .venv/bin/activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crear la base de datos en MySQL:

   ```sql
   CREATE DATABASE scenthub_db CHARACTER SET utf8mb4;
   ```

5. Copiar `.env.example` a `.env` y completar con tus datos:

   ```bash
   cp .env.example .env
   ```

   Variables:
   - `FLASK_ENV`: `development` o `production`
   - `SECRET_KEY`: clave secreta de la aplicación (usar una aleatoria en producción)
   - `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME`: credenciales de MySQL

6. Aplicar las migraciones:

   ```bash
   flask db upgrade
   ```

7. (Opcional) Cargar datos de ejemplo (categorías, perfumes, un admin y un cliente):

   ```bash
   python seed.py
   ```

   Usuario admin de prueba: `admin@scenthub.com` / `admin123`

8. Levantar el servidor de desarrollo:

   ```bash
   python run.py
   ```

   La aplicación queda disponible en `http://localhost:5000`.

## Despliegue en producción

1. En el servidor, configurar las variables de entorno (archivo `.env` o
   variables del sistema), con `FLASK_ENV=production` y un `SECRET_KEY`
   robusto y único.

2. Instalar dependencias (incluye `gunicorn`, servidor WSGI para producción;
   requiere Linux/macOS — no está soportado en Windows):

   ```bash
   pip install -r requirements.txt
   ```

3. Aplicar migraciones:

   ```bash
   flask db upgrade
   ```

4. Levantar la aplicación con Gunicorn:

   ```bash
   gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```

   Se recomienda ejecutar Gunicorn detrás de un proxy inverso (Nginx) y
   como servicio administrado (systemd, Supervisor, etc.).

## Estructura del proyecto

```
app/
  blueprints/
    public/    → tienda, carrito, pago, pedidos
    auth/      → login, registro, logout
    admin/     → panel de administración
  models/      → Usuario, Categoria, Producto, Pedido, DetallePedido
  static/
    css/       → estilos propios (style.css)
    img/       → imágenes de productos subidas desde el panel admin
  templates/
migrations/    → migraciones de base de datos (Flask-Migrate / Alembic)
run.py         → punto de entrada para desarrollo
wsgi.py        → punto de entrada para producción (Gunicorn)
seed.py        → datos de ejemplo
```
