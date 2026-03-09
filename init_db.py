from app import app, db
from models import Categoria, User

with app.app_context():
    db.create_all()
    
    # Crear categorías por defecto
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
    
    db.session.commit()
    print("Base de datos inicializada correctamente.")
