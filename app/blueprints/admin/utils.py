import os
import uuid

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def guardar_imagen_producto(file_storage):
    """Guarda la imagen subida con un nombre único y devuelve el nombre de archivo.

    Devuelve None si no se envió ningún archivo (permite dejar el producto sin imagen).
    """
    if not isinstance(file_storage, FileStorage) or not file_storage.filename:
        return None

    extension = secure_filename(file_storage.filename).rsplit('.', 1)[-1].lower()
    nombre_archivo = f"{uuid.uuid4().hex}.{extension}"

    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    file_storage.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_archivo))

    return nombre_archivo


def eliminar_imagen_producto(nombre_archivo):
    """Elimina del disco una imagen de producto previamente guardada, si existe."""
    if not nombre_archivo:
        return

    ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_archivo)
    if os.path.isfile(ruta):
        os.remove(ruta)
