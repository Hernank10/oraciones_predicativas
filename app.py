import os
import json
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from config import Config
from models import db, User, Categoria, Ejemplo, Ejercicio, ProgresoUsuario, ResultadoEvaluacion, Recurso
from forms import (LoginForm, RegistroForm, EjemploForm, EjercicioForm, 
                   BuscarForm, EvaluacionForm)

# Inicializar aplicación
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Decorador para administradores
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Rutas principales
@app.route('/')
def index():
    categorias = Categoria.query.order_by(Categoria.orden).all()
    total_ejemplos = Ejemplo.query.count()
    total_usuarios = User.query.count()
    return render_template('index.html', 
                         categorias=categorias,
                         total_ejemplos=total_ejemplos,
                         total_usuarios=total_usuarios)

@app.route('/teoria')
def teoria():
    categorias = Categoria.query.order_by(Categoria.orden).all()
    return render_template('teoria.html', categorias=categorias)

@app.route('/teoria/<int:categoria_id>')
def teoria_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    ejemplos = Ejemplo.query.filter_by(categoria_id=categoria_id, activo=True).all()
    return render_template('teoria_detalle.html', categoria=categoria, ejemplos=ejemplos)

@app.route('/ejemplos')
def ejemplos():
    page = request.args.get('page', 1, type=int)
    categoria_id = request.args.get('categoria', type=int)
    
    query = Ejemplo.query.filter_by(activo=True)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    
    ejemplos_paginados = query.paginate(page=page, per_page=10)
    categorias = Categoria.query.all()
    
    return render_template('ejemplos.html', 
                         ejemplos=ejemplos_paginados,
                         categorias=categorias,
                         categoria_seleccionada=categoria_id)

@app.route('/ejemplo/<int:ejemplo_id>')
def ejemplo_detalle(ejemplo_id):
    ejemplo = Ejemplo.query.get_or_404(ejemplo_id)
    return render_template('ejemplo_detalle.html', ejemplo=ejemplo)

@app.route('/ejercicios')
def ejercicios():
    form = BuscarForm()
    categoria_id = request.args.get('categoria', type=int)
    dificultad = request.args.get('dificultad', type=int)
    
    query = Ejercicio.query.filter_by(activo=True)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if dificultad:
        query = query.filter_by(dificultad=dificultad)
    
    ejercicios = query.order_by(Ejercicio.dificultad).all()
    categorias = Categoria.query.all()
    
    return render_template('ejercicios.html', 
                         ejercicios=ejercicios,
                         categorias=categorias,
                         form=form)

@app.route('/ejercicio/<int:ejercicio_id>')
@login_required
def ejercicio_detalle(ejercicio_id):
    ejercicio = Ejercicio.query.get_or_404(ejercicio_id)
    return render_template('ejercicio_detalle.html', ejercicio=ejercicio)

@app.route('/verificar_ejercicio', methods=['POST'])
@login_required
def verificar_ejercicio():
    data = request.json
    ejercicio_id = data.get('ejercicio_id')
    respuesta = data.get('respuesta')
    
    ejercicio = Ejercicio.query.get_or_404(ejercicio_id)
    
    # Verificar respuesta
    es_correcta = (respuesta == ejercicio.respuesta_correcta)
    
    # Actualizar progreso
    progreso = ProgresoUsuario.query.filter_by(
        usuario_id=current_user.id,
        categoria_id=ejercicio.categoria_id
    ).first()
    
    if not progreso:
        progreso = ProgresoUsuario(
            usuario_id=current_user.id,
            categoria_id=ejercicio.categoria_id
        )
        db.session.add(progreso)
    
    if es_correcta:
        progreso.ejercicios_completados += 1
        progreso.puntuacion_total += ejercicio.puntos
    
    db.session.commit()
    
    return jsonify({
        'correcta': es_correcta,
        'explicacion': ejercicio.explicacion,
        'puntos_obtenidos': ejercicio.puntos if es_correcta else 0
    })

@app.route('/evaluacion')
@login_required
def evaluacion():
    form = EvaluacionForm()
    # Seleccionar ejercicios aleatorios
    ejercicios = Ejercicio.query.filter_by(activo=True).order_by(db.func.random()).limit(10).all()
    session['evaluacion_actual'] = [e.id for e in ejercicios]
    session['evaluacion_inicio'] = datetime.now().timestamp()
    return render_template('evaluacion.html', ejercicios=ejercicios, form=form)

@app.route('/enviar_evaluacion', methods=['POST'])
@login_required
def enviar_evaluacion():
    data = request.json
    respuestas = data.get('respuestas', [])
    tiempo_fin = datetime.now().timestamp()
    tiempo_inicio = session.get('evaluacion_inicio', tiempo_fin)
    
    ejercicios_ids = session.get('evaluacion_actual', [])
    ejercicios = Ejercicio.query.filter(Ejercicio.id.in_(ejercicios_ids)).all()
    
    puntuacion = 0
    respuestas_detalle = []
    
    for i, ejercicio in enumerate(ejercicios):
        respuesta = respuestas[i] if i < len(respuestas) else None
        es_correcta = (respuesta == ejercicio.respuesta_correcta)
        if es_correcta:
            puntuacion += ejercicio.puntos
        respuestas_detalle.append({
            'ejercicio_id': ejercicio.id,
            'respuesta': respuesta,
            'correcta': es_correcta
        })
    
    resultado = ResultadoEvaluacion(
        usuario_id=current_user.id,
        puntuacion=puntuacion,
        total_preguntas=len(ejercicios),
        tiempo_empleado=int(tiempo_fin - tiempo_inicio),
        respuestas=respuestas_detalle
    )
    
    db.session.add(resultado)
    db.session.commit()
    
    session.pop('evaluacion_actual', None)
    session.pop('evaluacion_inicio', None)
    
    return jsonify({
        'puntuacion': puntuacion,
        'total': len(ejercicios),
        'resultado_id': resultado.id
    })

@app.route('/resultados/<int:resultado_id>')
@login_required
def ver_resultados(resultado_id):
    resultado = ResultadoEvaluacion.query.get_or_404(resultado_id)
    if resultado.usuario_id != current_user.id:
        flash('No puedes ver resultados de otros usuarios.', 'danger')
        return redirect(url_for('index'))
    return render_template('resultados.html', resultado=resultado)

@app.route('/progreso')
@login_required
def progreso():
    progresos = ProgresoUsuario.query.filter_by(usuario_id=current_user.id).all()
    resultados_recientes = ResultadoEvaluacion.query.filter_by(
        usuario_id=current_user.id
    ).order_by(ResultadoEvaluacion.fecha.desc()).limit(5).all()
    
    # Estadísticas
    total_ejercicios = sum(p.ejercicios_completados for p in progresos)
    puntuacion_total = sum(p.puntuacion_total for p in progresos)
    
    return render_template('progreso.html',
                         progresos=progresos,
                         resultados_recientes=resultados_recientes,
                         total_ejercicios=total_ejercicios,
                         puntuacion_total=puntuacion_total)

@app.route('/buscar')
def buscar():
    form = BuscarForm(request.args)
    if form.validate():
        query = form.query.data
        resultados_ejemplos = Ejemplo.query.filter(
            Ejemplo.texto.contains(query),
            Ejemplo.activo == True
        ).limit(10).all()
        
        resultados_ejercicios = Ejercicio.query.filter(
            Ejercicio.pregunta.contains(query),
            Ejercicio.activo == True
        ).limit(10).all()
        
        return render_template('buscar.html',
                             query=query,
                             ejemplos=resultados_ejemplos,
                             ejercicios=resultados_ejercicios)
    return redirect(url_for('index'))

@app.route('/recursos')
def recursos():
    recursos = Recurso.query.order_by(Recurso.fecha_publicacion.desc()).all()
    return render_template('recursos.html', recursos=recursos)

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'¡Bienvenido de nuevo, {user.nombre}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('registro.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('El email ya está registrado.', 'danger')
            return render_template('registro.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            nombre=form.nombre.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('¡Registro completado con éxito!', 'success')
        return redirect(url_for('index'))
    
    return render_template('registro.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

# Rutas de administración
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_usuarios = User.query.count()
    total_ejemplos = Ejemplo.query.count()
    total_ejercicios = Ejercicio.query.count()
    usuarios_recientes = User.query.order_by(User.fecha_registro.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_usuarios=total_usuarios,
                         total_ejemplos=total_ejemplos,
                         total_ejercicios=total_ejercicios,
                         usuarios_recientes=usuarios_recientes)

@app.route('/admin/ejemplos')
@login_required
@admin_required
def admin_ejemplos():
    ejemplos = Ejemplo.query.order_by(Ejemplo.fecha_creacion.desc()).all()
    return render_template('admin/gestionar_ejemplos.html', ejemplos=ejemplos)

@app.route('/admin/ejemplos/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_nuevo_ejemplo():
    form = EjemploForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        ejemplo = Ejemplo(
            texto=form.texto.data,
            analisis=form.analisis.data,
            categoria_id=form.categoria_id.data,
            dificultad=form.dificultad.data,
            usuario_id=current_user.id
        )
        db.session.add(ejemplo)
        db.session.commit()
        flash('Ejemplo creado correctamente.', 'success')
        return redirect(url_for('admin_ejemplos'))
    
    return render_template('admin/editar_ejemplo.html', form=form, modo='nuevo')

@app.route('/admin/ejemplos/editar/<int:ejemplo_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_editar_ejemplo(ejemplo_id):
    ejemplo = Ejemplo.query.get_or_404(ejemplo_id)
    form = EjemploForm(obj=ejemplo)
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        ejemplo.texto = form.texto.data
        ejemplo.analisis = form.analisis.data
        ejemplo.categoria_id = form.categoria_id.data
        ejemplo.dificultad = form.dificultad.data
        db.session.commit()
        flash('Ejemplo actualizado correctamente.', 'success')
        return redirect(url_for('admin_ejemplos'))
    
    return render_template('admin/editar_ejemplo.html', form=form, ejemplo=ejemplo, modo='editar')

@app.route('/admin/ejemplos/eliminar/<int:ejemplo_id>')
@login_required
@admin_required
def admin_eliminar_ejemplo(ejemplo_id):
    ejemplo = Ejemplo.query.get_or_404(ejemplo_id)
    ejemplo.activo = False
    db.session.commit()
    flash('Ejemplo desactivado correctamente.', 'success')
    return redirect(url_for('admin_ejemplos'))

@app.route('/admin/ejercicios')
@login_required
@admin_required
def admin_ejercicios():
    ejercicios = Ejercicio.query.all()
    return render_template('admin/gestionar_ejercicios.html', ejercicios=ejercicios)

@app.route('/admin/ejercicios/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_nuevo_ejercicio():
    form = EjercicioForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        # Convertir opciones de texto a lista
        opciones = [o.strip() for o in form.opciones.data.split('\n') if o.strip()]
        
        ejercicio = Ejercicio(
            pregunta=form.pregunta.data,
            tipo=form.tipo.data,
            opciones=opciones,
            respuesta_correcta=form.respuesta_correcta.data,
            explicacion=form.explicacion.data,
            categoria_id=form.categoria_id.data,
            dificultad=form.dificultad.data,
            puntos=form.puntos.data
        )
        db.session.add(ejercicio)
        db.session.commit()
        flash('Ejercicio creado correctamente.', 'success')
        return redirect(url_for('admin_ejercicios'))
    
    return render_template('admin/editar_ejercicio.html', form=form, modo='nuevo')

# API endpoints para datos dinámicos
@app.route('/api/ejemplos/random')
def api_ejemplos_random():
    count = request.args.get('count', 5, type=int)
    ejemplos = Ejemplo.query.filter_by(activo=True).order_by(db.func.random()).limit(count).all()
    return jsonify([{
        'id': e.id,
        'texto': e.texto,
        'categoria': e.categoria.nombre,
        'analisis': e.analisis
    } for e in ejemplos])

@app.route('/api/estadisticas/usuario')
@login_required
def api_estadisticas_usuario():
    progresos = ProgresoUsuario.query.filter_by(usuario_id=current_user.id).all()
    resultados = ResultadoEvaluacion.query.filter_by(usuario_id=current_user.id).all()
    
    return jsonify({
        'progreso_categorias': [{
            'categoria': p.categoria.nombre,
            'ejercicios_completados': p.ejercicios_completados,
            'puntuacion': p.puntuacion_total
        } for p in progresos],
        'resultados': [{
            'fecha': r.fecha.isoformat(),
            'puntuacion': r.puntuacion,
            'total': r.total_preguntas
        } for r in resultados[-10:]]  # Últimos 10 resultados
    })

# Inicializar datos de ejemplo
@app.cli.command("init-db")
def init_db_command():
    """Inicializar la base de datos con datos de ejemplo."""
    db.create_all()
    
    # Crear categorías
    categorias = [
        {'nombre': 'Transitivas', 'descripcion': 'Oraciones que llevan complemento directo', 'icono': 'bi-arrow-right-circle', 'orden': 1},
        {'nombre': 'Intransitivas', 'descripcion': 'Oraciones que no llevan complemento directo', 'icono': 'bi-arrow-left-circle', 'orden': 2},
        {'nombre': 'Reflexivas', 'descripcion': 'La acción recae sobre el sujeto', 'icono': 'bi-arrow-repeat', 'orden': 3},
        {'nombre': 'Recíprocas', 'descripcion': 'Acción mutua entre sujetos', 'icono': 'bi-arrows', 'orden': 4},
        {'nombre': 'Predicación completa', 'descripcion': 'El verbo expresa todo sin complementos', 'icono': 'bi-check-circle', 'orden': 5},
        {'nombre': 'Predicación incompleta', 'descripcion': 'El verbo necesita complementos', 'icono': 'bi-exclamation-circle', 'orden': 6},
    ]
    
    for cat_data in categorias:
        if not Categoria.query.filter_by(nombre=cat_data['nombre']).first():
            cat = Categoria(**cat_data)
            db.session.add(cat)
    
    # Crear usuario admin
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@ejemplo.com',
            nombre='Administrador',
            es_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    db.session.commit()
    print("Base de datos inicializada correctamente.")

if __name__ == '__main__':
    app.run(debug=True)
