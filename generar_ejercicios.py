import json
import random

def generar_ejercicios():
    ejercicios = []
    
    # Tipos de ejercicios y sus configuraciones
    tipos = {
        'identificar': {
            'categorias': ['Transitivas', 'Intransitivas', 'Reflexivas', 'Recíprocas'],
            'plantillas': [
                {'pregunta': '¿Qué tipo de oración es? "{texto}"', 
                 'opciones': ['Transitiva', 'Intransitiva', 'Reflexiva', 'Recíproca']}
            ]
        },
        'completar': {
            'categorias': ['Complemento Directo', 'Complemento Indirecto', 'Complementos Circunstanciales'],
            'plantillas': [
                {'pregunta': 'Completa con el complemento {tipo}: "{texto}"',
                 'opciones': ['opcion1', 'opcion2', 'opcion3', 'opcion4']}
            ]
        }
    }
    
    # Datos de ejemplo para generar variaciones
    ejemplos_base = [
        {'texto': 'El niño come ___', 'tipo': 'CD', 'respuesta': 'una manzana'},
        {'texto': 'María envió una carta ___', 'tipo': 'CI', 'respuesta': 'a su abuela'},
        {'texto': 'Estudió ___', 'tipo': 'CC', 'respuesta': 'en la biblioteca'},
        {'texto': 'Los pájaros cantan ___', 'tipo': 'CC', 'respuesta': 'al amanecer'},
        {'texto': 'El perro persigue ___', 'tipo': 'CD', 'respuesta': 'al gato'},
        {'texto': 'Compré un regalo ___', 'tipo': 'CI', 'respuesta': 'para mi hermano'},
        {'texto': 'Viajaremos ___', 'tipo': 'CC', 'respuesta': 'mañana'},
        {'texto': 'Escribió una novela ___', 'tipo': 'CC', 'respuesta': 'con entusiasmo'}
    ]
    
    for i in range(1, 101):
        tipo = random.choice(['identificar', 'completar', 'gramatical', 'analisis', 'transformar', 'error', 'clasificar', 'teoria'])
        
        ejercicio = {
            'id': i,
            'tipo': tipo,
            'pregunta': f'Ejercicio {i} de práctica',
            'opciones': ['Opción A', 'Opción B', 'Opción C', 'Opción D'],
            'respuesta_correcta': random.randint(0, 3),
            'explicacion': f'Explicación detallada para el ejercicio {i}',
            'categoria': random.choice(['Transitivas', 'Intransitivas', 'Reflexivas', 'Recíprocas', 'Complemento Directo', 'Complemento Indirecto', 'Complementos Circunstanciales', 'Uso de preposiciones']),
            'dificultad': random.randint(1, 4),
            'pistas': [f'Pista 1 para ejercicio {i}', f'Pista 2 para ejercicio {i}']
        }
        
        ejercicios.append(ejercicio)
    
    return {'ejercicios': ejercicios}

if __name__ == '__main__':
    data = generar_ejercicios()
    with open('app/static/data/ejercicios_flashcards.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ 100 ejercicios generados correctamente")
