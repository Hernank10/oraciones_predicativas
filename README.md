# 📚 Oraciones Predicativas - Plataforma Educativa Interactiva

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Aplicación web completa para el aprendizaje de oraciones predicativas en español, desarrollada con Flask. Incluye teoría, ejemplos, ejercicios interactivos, flashcards y sistema de gamificación.

## ✨ Características Principales

### 📖 Contenido Educativo
- **Teoría completa** sobre oraciones predicativas
- **100+ ejemplos** clasificados por categorías
- **Explicaciones detalladas** de cada concepto gramatical
- **Análisis sintáctico** paso a paso

### 🎴 Flashcards Interactivas (NUEVO)
- **100 ejercicios** con diferentes tipos:
  - 🔍 Identificar tipo de oración
  - ✏️ Completar con complementos
  - ✅ Corregir errores gramaticales
  - 🔄 Transformar oraciones
  - 📊 Análisis sintáctico
- **Retroalimentación inmediata** con explicaciones
- **Sistema de pistas** para ayudar en ejercicios difíciles

### 🎮 Modos de Estudio
| Modo | Descripción | Características |
|------|-------------|-----------------|
| **Flashcards** | Modo estudio tradicional | Tarjetas volteables, aprendizaje a tu ritmo |
| **Práctica** | Ejercicios sin presión | Feedback inmediato, sin límite de tiempo |
| **Examen** | Pon a prueba tus conocimientos | 15 minutos, 20 ejercicios aleatorios |

### 🏆 Sistema de Gamificación
- **8 logros desbloqueables**:
  - 🌱 Principiante (10 ejercicios)
  - 📚 Estudiante (25 ejercicios)
  - 🎓 Avanzado (50 ejercicios)
  - 🏆 Experto (100 ejercicios)
  - 🔥 En racha (5 seguidas)
  - ⚡ Imparable (10 seguidas)
  - 💯 Perfecto (100% en categoría)
  - 🌅 Madrugador (práctica antes de 8 AM)
- **Rachas de aciertos** con contador visual
- **Confetti** al desbloquear logros
- **Estadísticas detalladas** por categoría

### 👥 Gestión de Usuarios
- Registro y autenticación segura
- Perfiles personalizados
- Seguimiento de progreso individual
- Historial de evaluaciones

### 📊 Dashboard de Progreso
- Gráficos interactivos con Chart.js
- Estadísticas en tiempo real
- Progreso por categoría
- Comparativa de rendimiento

### 🛠️ Panel de Administración
- Gestión completa de ejemplos
- Administración de ejercicios
- Estadísticas globales
- Usuarios y permisos

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Hernank10/oraciones_predicativas.git
cd oraciones_predicativas

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Inicializar base de datos
python init_db.py

# 6. Ejecutar la aplicación
python app.py

# Oraciones Predicativas - Plataforma Educativa

Aplicación web para el aprendizaje de oraciones predicativas en español.

## CaracterísticasLa aplicación estará disponible en: http://localhost:5000

🎯 Usuarios por Defecto
Tipo	Usuario	Contraseña	Permisos
Administrador	admin	admin123	Acceso completo
Usuario regular	(registrarse)	(elegir)	Progreso personal
📁 Estructura del Proyecto
text
oraciones_predicativas/
├── 📄 app.py                 # Aplicación principal Flask
├── 📄 models.py              # Modelos de base de datos
├── 📄 forms.py               # Formularios WTForms
├── 📄 config.py              # Configuración
├── 📄 init_db.py             # Inicializador de BD
├── 📄 requirements.txt       # Dependencias
├── 📄 .gitignore             # Archivos ignorados por Git
├── 📄 README.md              # Este archivo
├── 📄 DEPLOY.md              # Instrucciones de despliegue
│
├── 📁 app/
│   ├── 📁 static/
│   │   ├── 📁 css/
│   │   │   └── 🎨 style.css  # Estilos personalizados
│   │   ├── 📁 js/
│   │   │   └── ⚡ main.js     # JavaScript interactivo
│   │   └── 📁 data/
│   │       └── 📊 ejercicios_flashcards.json  # 100 ejercicios
│   │
│   └── 📁 templates/
│       ├── 📄 base.html        # Plantilla base
│       ├── 📄 index.html        # Página principal
│       ├── 📄 login.html        # Inicio de sesión
│       ├── 📄 registro.html     # Registro de usuarios
│       ├── 📄 teoria.html       # Teoría gramatical
│       ├── 📄 ejemplos.html     # Ejemplos clasificados
│       ├── 📄 ejercicios.html   # Lista de ejercicios
│       ├── 📄 flashcards.html   # ¡NUEVO! Flashcards interactivas
│       ├── 📄 progreso.html     # Progreso del usuario
│       └── 📄 resultados.html   # Resultados de evaluaciones
│
└── 📁 instance/
    └── 🗄️ oraciones.db         # Base de datos SQLite
🎨 Capturas de Pantalla
Página Principal
text
🏠 Vista de inicio con categorías y estadísticas
Flashcards Interactivas
text
🎴 Interfaz de estudio con tarjetas volteables
Dashboard de Progreso
text
📊 Gráficos y estadísticas de rendimiento
🔧 Tecnologías Utilizadas
Tecnología	Versión	Uso
Flask	2.3.3	Framework web principal
SQLAlchemy	3.0.5	ORM para base de datos
Bootstrap 5	5.3	Frontend y diseño responsive
jQuery	3.6	Interactividad en cliente
Chart.js	4.0	Gráficos y visualizaciones
Flask-Login	0.6.2	Autenticación de usuarios
Flask-WTF	1.1.1	Formularios seguros
SQLite	-	Base de datos ligera
🤝 Cómo Contribuir
¡Las contribuciones son bienvenidas! Sigue estos pasos:

Fork el proyecto

Crea tu rama de características:

bash
git checkout -b feature/NuevaCaracteristica
Commit tus cambios:

bash
git commit -m 'Add: nueva característica increíble'
Push a la rama:

bash
git push origin feature/NuevaCaracteristica
Abre un Pull Request

📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

👨‍💻 Autor
Hernank10

GitHub: @Hernank10

Proyecto: Oraciones Predicativas

🌟 Reconocimientos
A todos los estudiantes que usarán esta plataforma

A la comunidad de Flask por el excelente framework

A Bootstrap por el diseño responsive

A los contribuidores que ayudarán a mejorar el proyecto

📊 Estadísticas del Proyecto
⭐ Estrellas: 0 (¡tú puedes ser el primero!)

🍴 Forks: 0

📝 Commits: Primer versión

🎯 Ejercicios: 100+

👥 Usuarios potenciales: Ilimitados

🚀 Próximas Mejoras
Más ejercicios (objetivo: 500)

Modo multijugador

Exportar a PDF los resultados

App móvil nativa con Kivy

Reconocimiento de voz para práctica oral

Integración con Google Classroom

Más idiomas (inglés, portugués)

⭐ Si te gusta este proyecto, ¡no olvides darle una estrella en GitHub! ⭐

Hecho con ❤️ para la educación y el aprendizaje del español

- Teoría completa sobre oraciones predicativas
- Ejemplos clasificados por categorías
- Ejercicios interactivos
- Sistema de usuarios y progreso
- Evaluaciones personalizadas
- Panel de administración

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Hernank10/oraciones-predicativas.git
cd oraciones-predicativas
