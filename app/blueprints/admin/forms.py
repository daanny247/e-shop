from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'webp']
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB


class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre',
                validators=[DataRequired(), Length(min=2, max=80)])

    descripcion = TextAreaField('Descripción',
                validators=[Optional(), Length(max=200)])

    submit = SubmitField('Guardar')


class ProductoForm(FlaskForm):
    nombre = StringField('Nombre',
                validators=[DataRequired(), Length(min=2, max=150)])

    descripcion = TextAreaField('Descripción', validators=[Optional()])

    precio = DecimalField('Precio', places=2,
                validators=[DataRequired(), NumberRange(min=0.01, message='El precio debe ser mayor a 0')])

    stock = IntegerField('Stock',
                validators=[DataRequired(), NumberRange(min=0, message='El stock no puede ser negativo')])

    categoria_id = SelectField('Categoría', coerce=int,
                validators=[DataRequired(message='Selecciona una categoría')])

    imagen = FileField('Imagen (jpg, jpeg o webp, máx. 2MB)', validators=[
                Optional(),
                FileAllowed(ALLOWED_IMAGE_EXTENSIONS, 'Solo se permiten imágenes JPG, JPEG o WEBP'),
                FileSize(max_size=MAX_IMAGE_SIZE, message='La imagen no debe superar 2MB'),
            ])

    submit = SubmitField('Guardar')
