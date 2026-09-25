# 🚒 Bomberos Educa - Plataforma E-Learning

Plataforma web de capacitación para la Compañía de Bomberos de Maipú y Cerrillos, desarrollada como proyecto final de **Ingeniería de Software** en INACAP.

## 🎯 Descripción

Sistema E-Learning que permite gestionar cursos, módulos y contenidos educativos en múltiples formatos (texto, video, imagen, archivo), con sistema de evaluaciones automáticas y dashboard de KPIs para la toma de decisiones del Superintendente.

## 🛠️ Tecnologías

- **Backend:** Django 5.0.14
- **Frontend:** Bootstrap 5 + HTML5
- **Base de Datos:** SQLite3 (desarrollo)
- **Admin:** Jazzmin (tema personalizado rojo bombero)
- **Metodología:** Scrum

## 📋 Requisitos

- Python 3.12+
- pip
- Git

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MauricioPinoReyes/E-Learning-Bomberos-Educa.git
cd demo_e-learning_bomberos
```

### 2. Crear y activar entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

### 7. Acceder a la plataforma

- **Sitio principal:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

## 👥 Roles de Usuario

| Rol                                       | Descripción                                           |
| ----------------------------------------- | ------------------------------------------------------ |
| **Visitante**                       | Ve catálogo de cursos                                 |
| **Estudiante (Bombero)**            | Se inscribe, visualiza contenidos y rinde evaluaciones |
| **Instructor (Capitán)**           | Gestiona cursos y contenidos (CMS)                     |
| **Administrador (Superintendente)** | Dashboard de KPIs y gestión total                     |

## 📊 Funcionalidades Principales

- ✅ **CMS de instructores** con contenido polimórfico (Texto, Imagen, Video, Archivo)
- ✅ **Sistema de evaluaciones** con calificación automática y revisión de respuestas
- ✅ **Dashboard de KPIs** con indicadores de umbral (verde/rojo/gris)
- ✅ **Diseño 100% responsivo** con Bootstrap 5
- ✅ **Recuperación de contraseña** por email (en desarrollo)
- ✅ **Control de acceso basado en roles** (RBAC)
- ✅ **Drag & Drop** para reordenar módulos y contenidos
- ✅ **Tema personalizado** con Jazzmin (rojo bombero)

## 🧪 Pruebas

## 📁 Estructura del Proyecto

```
demo_e-learning_bomberos/
├── educa/              # Configuración del proyecto
├── courses/            # App de gestión de cursos y evaluaciones
├── students/           # App de estudiantes
├── templates/          # Templates globales
├── media/              # Archivos subidos (no incluido en git)
├── venv/               # Entorno virtual (no incluido en git)
├── manage.py
├── requirements.txt
└── README.md
```

## 📈 KPIs del Dashboard

1. **Total de alumnos inscritos** (matrículas activas)
2. **Alumnos que finalizaron** (aprobaciones únicas)
3. **Tiempo promedio de finalización** (días desde registro hasta aprobación)
4. **Promedio de notas** (de evaluaciones aprobadas)
5. **Indicadores de umbral** (verde/rojo/gris según metas)

**Asignatura:** Ingeniería de Software - INACAP 2026
**Sección:** V-FB50-N4-P14-C1

- **Richard Machuca** - Scrum Master
- **Mauricio Pino** - Developer (Backend)
- **Freddy Villaseca** - Developer (Frontend)
- **Jesus Hidalgo** - Developer (Testing)

## 📄 Licencia

Proyecto académico - Uso educacional.

---
