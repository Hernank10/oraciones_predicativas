from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, BooleanField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])

class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre completo', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar contraseña', 
                                     validators=[DataRequired(), EqualTo('password')])

class EjemploForm(FlaskForm):
    texto = TextAreaField('Texto del ejemplo', validators=[DataRequired(), Length(max=500)])
    analisis = TextAreaField('Análisis', validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    dificultad = IntegerField('Dificultad (1-5)', validators=[NumberRange(min=1, max=5)], default=1)

class EjercicioForm(FlaskForm):
    pregunta = TextAreaField('Pregunta', validators=[DataRequired()])
    tipo = SelectField('Tipo de ejercicio', choices=[
        ('opcion_multiple', 'Opción múltiple'),
        ('completar', 'Completar espacios'),
        ('identificar', 'Identificar tipo')
    ])
    opciones = TextAreaField('Opciones (una por línea)')
    respuesta_correcta = IntegerField('Respuesta correcta (índice)', validators=[DataRequired()])
    explicacion = TextAreaField('Explicación')
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    dificultad = IntegerField('Dificultad (1-5)', validators=[NumberRange(min=1, max=5)], default=1)
    puntos = IntegerField('Puntos', default=10)

class BuscarForm(FlaskForm):
    query = StringField('Buscar', validators=[DataRequired()])

class EvaluacionForm(FlaskForm):
    respuestas = TextAreaField('Respuestas')  # Se manejará con JavaScript
