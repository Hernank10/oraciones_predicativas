from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(100))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    es_admin = db.Column(db.Boolean, default=False)
    
    progresos = db.relationship('ProgresoUsuario', backref='usuario', lazy=True)
    resultados = db.relationship('ResultadoEvaluacion', backref='usuario', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    icono = db.Column(db.String(20), default='bi-folder')
    orden = db.Column(db.Integer, default=0)
    
    ejemplos = db.relationship('Ejemplo', backref='categoria', lazy=True)
    ejercicios = db.relationship('Ejercicio', backref='categoria', lazy=True)

class Ejemplo(db.Model):
    __tablename__ = 'ejemplos'
    
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(500), nullable=False)
    analisis = db.Column(db.Text)
    dificultad = db.Column(db.Integer, default=1)  # 1-5
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

class Ejercicio(db.Model):
    __tablename__ = 'ejercicios'
    
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.Text, nullable=False)
    opciones = db.Column(db.JSON)  # Guardar como JSON
    respuesta_correcta = db.Column(db.Integer)
    explicacion = db.Column(db.Text)
    tipo = db.Column(db.String(20))  # 'opcion_multiple', 'completar', 'identificar'
    dificultad = db.Column(db.Integer, default=1)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    puntos = db.Column(db.Integer, default=10)
    activo = db.Column(db.Boolean, default=True)

class ProgresoUsuario(db.Model):
    __tablename__ = 'progreso_usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    ejercicios_completados = db.Column(db.Integer, default=0)
    puntuacion_total = db.Column(db.Integer, default=0)
    ultimo_acceso = db.Column(db.DateTime, default=datetime.utcnow)
    nivel_dominio = db.Column(db.Float, default=0.0)  # 0-100%

class ResultadoEvaluacion(db.Model):
    __tablename__ = 'resultados_evaluacion'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    puntuacion = db.Column(db.Integer)
    total_preguntas = db.Column(db.Integer)
    tiempo_empleado = db.Column(db.Integer)  # en segundos
    respuestas = db.Column(db.JSON)  # Guardar respuestas del usuario

class Recurso(db.Model):
    __tablename__ = 'recursos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(20))  # 'pdf', 'video', 'enlace'
    url = db.Column(db.String(200))
    archivo = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    descargas = db.Column(db.Integer, default=0)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
