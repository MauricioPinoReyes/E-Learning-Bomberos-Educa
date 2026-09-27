# 🚒 Bomberos Educa — Plataforma E-Learning

[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)](https://getbootstrap.com/)
[![Tests](<https://img.shields.io/badge/Tests-42%20passing-brightgreen>)](#-pruebas)
[![License](https://img.shields.io/badge/License-Académica-blue)](#-licencia)

Plataforma web de capacitación para la **Compañía de Bomberos de Maipú y Cerrillos**, desarrollada como proyecto final de **Ingeniería de Software** en INACAP.

---

## 🎯 Descripción

Sistema E-Learning que permite gestionar cursos, módulos y contenidos educativos en múltiples formatos (texto, video, imagen, archivo), con sistema de evaluaciones automáticas y dashboard de KPIs para la toma de decisiones del Superintendente.

---

## 🛠️ Tecnologías

| Tecnología                  | Versión | Uso                           |
| ---------------------------- | -------- | ----------------------------- |
| **Django**             | 5.0      | Framework principal (MTV)     |
| **Python**             | 3.12+    | Lenguaje base                 |
| **Bootstrap**          | 5.3      | Frontend responsivo           |
| **SQLite**             | 3        | Base de datos (desarrollo)    |
| **Jazzmin**            | 3.0      | Tema del admin (rojo bombero) |
| **django-embed-video** | 1.4      | Integración de videos        |
| **Pillow**             | 10+      | Manejo de imágenes           |
| **Scrum**              | —       | Metodología ágil            |

---

## 📋 Requisitos previos

- **Python** 3.12 o superior
- **pip** (gestor de paquetes)
- **Git** (control de versiones)
- **Navegador moderno** (Chrome, Firefox, Edge)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MauricioPinoReyes/E-Learning-Bomberos-Educa.git
cd E-Learning-Bomberos-Educa
```

### 2. Crear y activar entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
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

### 5. Crear superusuario (admin)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

### 7. Acceder a la plataforma

| Servicio                  | URL                                         |
| ------------------------- | ------------------------------------------- |
| **Sitio principal** | http://127.0.0.1:8000/                      |
| **Admin (Jazzmin)** | http://127.0.0.1:8000/admin/                |
| **Dashboard KPIs**  | http://127.0.0.1:8000/admin/dashboard-kpis/ |

---

## 👥 Roles de usuario

| Rol                                       | Descripción                                   | Permisos                   |
| ----------------------------------------- | ---------------------------------------------- | -------------------------- |
| **Visitante**                       | Ve el catálogo de cursos                      | Lectura pública           |
| **Estudiante (Bombero)**            | Se inscribe, ve contenidos, rinde evaluaciones | Acceso a cursos inscritos  |
| **Instructor (Capitán)**           | Gestiona cursos y contenidos (CMS)             | CRUD de sus propios cursos |
| **Administrador (Superintendente)** | Dashboard de KPIs y gestión total             | Acceso completo            |

### Flujo de login inteligente

Al iniciar sesión, el sistema redirige según el rol:

- **Instructor / Admin** → CMS de cursos (`/course/mine/`)
- **Estudiante** → "Mis cursos" (`/students/courses/`)

---

## 📊 Funcionalidades principales

- ✅ **CMS de instructores** con contenido polimórfico (Texto, Imagen, Video, Archivo)
- ✅ **Sistema de evaluaciones** con calificación automática y revisión de respuestas
- ✅ **Dashboard de KPIs** con indicadores de umbral (verde/rojo/gris)
- ✅ **Diseño 100% responsivo** con Bootstrap 5
- ✅ **Recuperación de contraseña** por email (en desarrollo)
- ✅ **Control de acceso basado en roles** (RBAC)
- ✅ **Drag & Drop** para reordenar módulos y contenidos
- ✅ **Tema personalizado** con Jazzmin (rojo bombero)
- ✅ **Aislamiento de datos** por instructor (filtrado por `owner`)

---

## 🧪 Pruebas

La suite completa de pruebas está documentada en detalle en [`README_TESTS.md`](README_TESTS.md).

### Resumen

| Métrica                       | Valor           |
| ------------------------------ | --------------- |
| **Total de tests**       | 42              |
| **Tests exitosos**       | 42 (100%)       |
| **Tests fallidos**       | 0               |
| **Tiempo de ejecución** | ~18 segundos    |
| **Cobertura**            | ~80%            |
| **Framework**            | Django TestCase |

### Ejecutar las pruebas

```bash
# Toda la suite
python manage.py test courses

# Con detalle
python manage.py test courses -v 2

# Una clase específica
python manage.py test courses.tests.LoginValidCredentialsTest -v 2
```

### Estrategia de pruebas (pirámide)

```
         ▲
        / \
       /E2E\      ← 15 pruebas manuales (TP05–TP07)
      /-----\
     /Integra\    ← 12 pruebas de integración
    /---------\
   / Unitarias \  ← 27 pruebas unitarias
  /-------------\
```

### Cobertura por caso

- **TP01–TP14**: 14 casos de prueba documentados.
- **RF01–RF17**: 100% de los requisitos funcionales cubiertos.
- **RNF05, RNF06**: Seguridad verificada.

### Hallazgos documentados

| # | Hallazgo                                                 | Impacto  | Sprint   |
| - | -------------------------------------------------------- | -------- | -------- |
| 1 | Inconsistencia en cálculo de score (modelo vs. vista)   | 🔴 Alto  | Sprint 5 |
| 2 | `quiz_submit` sin validación de inscripción          | 🟡 Medio | Sprint 5 |
| 3 | `total_intentos` no está en el contexto del dashboard | 🟡 Medio | Sprint 5 |

> Para más detalles, consultar [`README_TESTS.md`](README_TESTS.md).

---

## 📁 Estructura del proyecto

```
E-Learning-Bomberos-Educa/
│
├── educa/                              # Configuración del proyecto
│   ├── settings.py                     # Configuración general
│   ├── urls.py                         # URLs raíz + smart_login_redirect
│   └── ...
│
├── courses/                            # App: gestión de cursos y evaluaciones
│   ├── models.py                       # Subject, Course, Module, Content, Quiz, ...
│   ├── views.py                        # CMS, catálogo, detalle
│   ├── admin.py                        # Admin con filtrado por owner
│   ├── admin_dashboard.py              # Vista del Dashboard de KPIs
│   ├── forms.py                        # ModuleFormSet
│   ├── fields.py                       # OrderField
│   ├── tests.py                        # 42 tests automatizados
│   ├── urls.py
│   ├── migrations/
│   └── templates/
│       └── courses/                    # Templates PROPIOS de courses
│           ├── course/                 # Catálogo y detalle
│           ├── manage/                 # CMS de instructores
│           └── content/                # Render de contenido polimórfico
│
├── students/                           # App: gestión de estudiantes
│   ├── views.py                        # Inscripción, quiz_take, quiz_submit
│   ├── forms.py                        # CourseEnrollForm
│   ├── urls.py
│   └── templates/
│       └── students/                   # Templates PROPIOS de students
│           ├── student/                # Registro
│           ├── course/                 # "Mis cursos"
│           └── quiz/                   # Rendir y ver resultado
│
├── templates/                          # Templates GLOBALES (compartidos)
│   ├── base.html                       # Layout principal
│   ├── registration/
│   │   ├── login.html                  # Login (auth de Django)
│   │   └── password_reset.html         # Recuperación de contraseña
│   └── admin/
│       └── dashboard_kpis.html         # Dashboard KPIs
│
├── media/                              # Archivos subidos (no en git)
├── venv/                               # Entorno virtual (no en git)
├── manage.py
├── requirements.txt
├── README.md
├── README_TESTS.md
└── .gitignore
```

---

## 🏛️ Separación de responsabilidades

El proyecto sigue el principio de **alta cohesión y bajo acoplamiento**, organizando el código en dos apps independientes:

| App                    | Responsabilidad                       | Modelos                                                                                                        | Templates                        |
| ---------------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **`courses`**  | Gestión de contenido educativo       | Subject, Course, Module, Content, Text, Image, File, Video, Quiz, Question, Answer, QuizAttempt, StudentAnswer | `courses/templates/courses/`   |
| **`students`** | Gestión de estudiantes y aprendizaje | Usa modelos de`courses`                                                                                      | `students/templates/students/` |

### Plantillas por app

- **`courses/templates/courses/`**: catálogo, detalle, CMS de instructores y render de contenido polimórfico.
- **`students/templates/students/`**: registro, "Mis cursos", rendir evaluación y resultados.
- **`templates/` (raíz)**: solo plantillas **globales** compartidas (`base.html`, login, dashboard).

Esta separación permite:

- ✅ Mantener cada app autocontenida.
- ✅ Facilitar el mantenimiento y la evolución.
- ✅ Evitar dependencias cruzadas innecesarias.
- ✅ Escalar el proyecto sin romper la estructura.

---

## 📈 KPIs del dashboard

El dashboard (`/admin/dashboard-kpis/`) muestra:

1. **Total de alumnos inscritos** — matrículas activas únicas.
2. **Alumnos que finalizaron** — usuarios que aprobaron al menos un quiz.
3. **Tiempo promedio de finalización** — días desde registro hasta aprobación.
4. **Promedio de notas** — media de todos los intentos completados.
5. **Indicadores de umbral** (verde/rojo/gris según metas configurables).

### Umbrales por defecto

| Umbral        | Valor    | Color si cumple | Color si no cumple |
| ------------- | -------- | --------------- | ------------------ |
| Meta de nota  | 70%      | 🟢 Verde        | 🔴 Rojo            |
| Meta de días | 14 días | 🟢 Verde        | 🔴 Rojo            |
| Sin datos     | —       | ⚪ Gris         | ⚪ Gris            |

---

## 🗺️ Roadmap

| Versión | Funcionalidad                             | Prioridad |
| -------- | ----------------------------------------- | --------- |
| v1.1     | Corrección de los 3 hallazgos de pruebas | 🔴 Alta   |
| v1.2     | Sistema de notificaciones por email       | 🟡 Media  |
| v1.3     | Certificados descargables en PDF          | 🟡 Media  |
| v2.0     | Migración a PostgreSQL                   | 🟡 Media  |
| v2.1     | Despliegue en AWS / Heroku                | 🟢 Baja   |
| v2.2     | App móvil nativa (React Native)          | 🟢 Baja   |

---

## 🤝 Contribución

Este es un proyecto académico. Para contribuir:

1. Haz un fork del repositorio.
2. Crea una rama con tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Ejecuta las pruebas antes de commitear (`python manage.py test courses`).
4. Sigue las convenciones de código PEP 8.
5. Envía un Pull Request describiendo los cambios.

---

## 📚 Documentación adicional

- [`README_TESTS.md`](README_TESTS.md) — Guía completa de pruebas
- [Anexo A — Pruebas manuales](docs/anexo_pruebas_manuales.md) — TP05, TP06, TP07
- [Informe de Ingeniería de Software](docs/informe.md) — Documento completo

---

## 👥 Autores

**Asignatura**: Ingeniería de Software — INACAP 2026
**Sección**: V-FB50-N4-P14-C1
**Académico**: Felipe Fuentes Ayar

| Rol                              | Integrante                |
| -------------------------------- | ------------------------- |
| **Product Owner**          | Prof. Felipe Fuentes Ayar |
| **Scrum Master**           | Richard Machuca           |
| **Developer (Backend)**    | Mauricio Pino             |
| **Developer (Frontend)**   | Freddy Villaseca          |
| **Developer (Testing/QA)** | Jesus Hidalgo             |

---

## 📄 Licencia

Proyecto académico de uso educacional. Todos los derechos reservados a los autores.

**INACAP** — Área Informática y Telecomunicaciones
**Ingeniería en Informática** — 2026

---

## 📅 Changelog

### v1.0 — 2026-09-23

- ✅ Lanzamiento inicial
- ✅ CMS de instructores con contenido polimórfico
- ✅ Sistema de evaluaciones
- ✅ Dashboard de KPIs
- ✅ 42 tests automatizados (100% exitosos)

### v1.1 — (pendiente)

- 🔄 Corrección de los 3 hallazgos detectados en pruebas
- 🔄 Sistema de notificaciones por email

---

> **Nota**: Este README se actualiza al final de cada sprint con los cambios más relevantes.



# ANEXO A — PRUEBAS MANUALES (TP01 – TP15)

## Introducción

Las pruebas manuales complementan la suite automatizada de 42 tests, validando
flujos completos de usuario que requieren interacción real con la interfaz web.

**Herramienta**: Navegador web (Chrome / Firefox / Edge)
**Entorno**: Servidor local (`python manage.py runserver`)
**Responsable**: Equipo de QA
**Fecha de ejecución**: ________________

### Leyenda

| Símbolo | Significado            |
| -------- | ---------------------- |
| ⬜       | Pendiente              |
| ✅       | Pasa                   |
| ❌       | Falla                  |
| ⚠️     | Pasa con observaciones |

---

## TP01 — Registro de nuevo estudiante

### Identificación

| Campo                        | Detalle                           |
| ---------------------------- | --------------------------------- |
| **ID**                 | TP01                              |
| **Nombre**             | Registro de nuevo estudiante      |
| **Tipo**               | Manual                            |
| **Prioridad**          | Alta                              |
| **Requisito cubierto** | RF01 (Autenticación de usuarios) |

### Precondiciones

- Servidor corriendo en `http://localhost:8000/`.
- Usuario NO registrado previamente con el username a usar.

### Datos de prueba

| Campo                 | Valor              |
| --------------------- | ------------------ |
| Usuario               | `bombero_test01` |
| Contraseña           | `TestPass123!`   |
| Confirmar contraseña | `TestPass123!`   |

### Pasos de ejecución

| # | Acción                                          | Resultado esperado                                 |
| - | ------------------------------------------------ | -------------------------------------------------- |
| 1 | Ir a`http://localhost:8000/students/register/` | Se muestra el formulario de registro               |
| 2 | Completar usuario y contraseñas                 | Campos aceptados sin errores                       |
| 3 | Click en "Registrarse"                           | Se crea la cuenta y se autentica automáticamente  |
| 4 | Verificar redirección                           | Redirige a "Mis cursos" (`/students/courses/`)   |
| 5 | Verificar sesión activa                         | El nombre del usuario aparece en la barra superior |

### Resultado esperado

El estudiante queda registrado, autenticado y redirigido a su panel.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP02 — Inicio de sesión con credenciales válidas

### Identificación

| Campo                        | Detalle                         |
| ---------------------------- | ------------------------------- |
| **ID**                 | TP02                            |
| **Nombre**             | Login con credenciales válidas |
| **Tipo**               | Manual                          |
| **Prioridad**          | Crítica                        |
| **Requisito cubierto** | RF01 (Autenticación)           |

### Precondiciones

- Usuario registrado previamente.

### Datos de prueba

| Campo       | Valor              |
| ----------- | ------------------ |
| Usuario     | `bombero_test01` |
| Contraseña | `TestPass123!`   |

### Pasos de ejecución

| # | Acción                  | Resultado esperado             |
| - | ------------------------ | ------------------------------ |
| 1 | Ir a`/accounts/login/` | Se muestra el formulario       |
| 2 | Ingresar credenciales    | Campos aceptados               |
| 3 | Click en "Entrar"        | Redirige según el rol         |
| 4 | Verificar sesión        | El usuario aparece autenticado |

### Resultado esperado

El usuario inicia sesión correctamente y es redirigido según su rol.

### Resultado obtenido

| Campo               | Detalle              |
| ------------------- | -------------------- |
| Estado              | ⬜ PASA  ⬜ FALLA    |
| URL de redirección | ____________________ |
| Observaciones       |                      |
| Evidencia           | Captura de pantalla  |

---

## TP03 — Inicio de sesión con credenciales inválidas

### Identificación

| Campo                        | Detalle                           |
| ---------------------------- | --------------------------------- |
| **ID**                 | TP03                              |
| **Nombre**             | Login con credenciales inválidas |
| **Tipo**               | Manual                            |
| **Prioridad**          | Alta                              |
| **Requisito cubierto** | RF01 (Autenticación)             |

### Precondiciones

- Usuario registrado previamente.

### Datos de prueba

| Campo       | Valor                         |
| ----------- | ----------------------------- |
| Usuario     | `bombero_test01`            |
| Contraseña | `WrongPass999` (incorrecta) |

### Pasos de ejecución

| # | Acción                                           | Resultado esperado                                                      |
| - | ------------------------------------------------- | ----------------------------------------------------------------------- |
| 1 | Ir a`/accounts/login/`                          | Se muestra el formulario                                                |
| 2 | Ingresar usuario válido + contraseña incorrecta | Campos aceptados                                                        |
| 3 | Click en "Entrar"                                 | El sistema rechaza el login                                             |
| 4 | Verificar mensaje de error                        | Aparece: "Por favor, introduzca un nombre de usuario y clave correctos" |
| 5 | Verificar sesión                                 | NO se crea sesión activa                                               |

### Resultado esperado

El sistema rechaza el login y muestra mensaje genérico (no revela si el usuario existe).

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP04 — Cierre de sesión

### Identificación

| Campo                        | Detalle               |
| ---------------------------- | --------------------- |
| **ID**                 | TP04                  |
| **Nombre**             | Cierre de sesión     |
| **Tipo**               | Manual                |
| **Prioridad**          | Media                 |
| **Requisito cubierto** | RF01 (Autenticación) |

### Precondiciones

- Usuario autenticado.

### Pasos de ejecución

| # | Acción                                   | Resultado esperado                     |
| - | ----------------------------------------- | -------------------------------------- |
| 1 | Estando autenticado, ir al menú superior | Se muestra la opción "Cerrar sesión" |
| 2 | Click en "Cerrar sesión"                 | Se cierra la sesión                   |
| 3 | Verificar redirección                    | Redirige al catálogo (`/`)          |
| 4 | Verificar sesión                         | El usuario ya no aparece autenticado   |
| 5 | Intentar acceder a`/students/courses/`  | Redirige a login                       |

### Resultado esperado

La sesión se cierra correctamente y el usuario pierde acceso a rutas protegidas.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP05 — Visualización del catálogo de cursos

### Identificación

| Campo                        | Detalle                      |
| ---------------------------- | ---------------------------- |
| **ID**                 | TP05                         |
| **Nombre**             | Catálogo público de cursos |
| **Tipo**               | Manual                       |
| **Prioridad**          | Alta                         |
| **Requisito cubierto** | RF06 (Catálogo de cursos)   |

### Precondiciones

- Existen cursos publicados en la plataforma.
- Usuario NO autenticado (para validar acceso público).

### Pasos de ejecución

| # | Acción                        | Resultado esperado                         |
| - | ------------------------------ | ------------------------------------------ |
| 1 | Ir a`http://localhost:8000/` | Se muestra el catálogo                    |
| 2 | Verificar listado de cursos    | Aparecen cursos con título y descripción |
| 3 | Verificar filtro por materia   | Se muestra la lista de materias            |
| 4 | Click en una materia           | Se filtran los cursos de esa materia       |
| 5 | Click en un curso              | Redirige al detalle del curso              |

### Resultado esperado

El catálogo es público, muestra cursos y permite filtrar por materia.

### Resultado obtenido

| Campo                   | Detalle             |
| ----------------------- | ------------------- |
| Estado                  | ⬜ PASA  ⬜ FALLA   |
| Nº de cursos mostrados | ____                |
| Observaciones           |                     |
| Evidencia               | Captura de pantalla |

---

## TP06 — Inscripción a un curso

### Identificación

| Campo                        | Detalle                               |
| ---------------------------- | ------------------------------------- |
| **ID**                 | TP06                                  |
| **Nombre**             | Inscripción de estudiante a un curso |
| **Tipo**               | Manual                                |
| **Prioridad**          | Alta                                  |
| **Requisito cubierto** | RF07 (Inscripción a cursos)          |

### Precondiciones

- Estudiante autenticado.
- Curso existente en el catálogo.
- El estudiante NO está inscrito previamente.

### Pasos de ejecución

| # | Acción                        | Resultado esperado              |
| - | ------------------------------ | ------------------------------- |
| 1 | Login como estudiante          | Redirige a "Mis cursos"         |
| 2 | Ir al catálogo (`/`)        | Se muestran los cursos          |
| 3 | Click en un curso              | Detalle del curso               |
| 4 | Click en "Inscribirse"         | Se procesa la inscripción      |
| 5 | Verificar redirección         | Redirige al detalle del curso   |
| 6 | Ir a "Mis cursos"              | El curso aparece en la lista    |
| 7 | Verificar botón "Inscribirse" | Ya NO se muestra para ese curso |

### Resultado esperado

El estudiante queda inscrito y el curso aparece en su panel personal.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP07 — Visualización de contenidos de un curso

### Identificación

| Campo                        | Detalle                                |
| ---------------------------- | -------------------------------------- |
| **ID**                 | TP07                                   |
| **Nombre**             | Visualización de contenidos del curso |
| **Tipo**               | Manual                                 |
| **Prioridad**          | Alta                                   |
| **Requisito cubierto** | RF08 (Visualización de lecciones)     |

### Precondiciones

- Estudiante inscrito en un curso.
- El curso tiene módulos con contenido de distintos tipos.

### Pasos de ejecución

| # | Acción                                   | Resultado esperado           |
| - | ----------------------------------------- | ---------------------------- |
| 1 | Login como estudiante inscrito            | Redirige a "Mis cursos"      |
| 2 | Click en el curso                         | Detalle con módulos         |
| 3 | Click en un módulo                       | Se muestran los contenidos   |
| 4 | Verificar contenido tipo**texto**   | Se renderiza correctamente   |
| 5 | Verificar contenido tipo**video**   | El video se embebe           |
| 6 | Verificar contenido tipo**imagen**  | La imagen se muestra         |
| 7 | Verificar contenido tipo**archivo** | Se ofrece enlace de descarga |

### Resultado esperado

Todos los tipos de contenido se renderizan correctamente.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP08 — Rendir evaluación y aprobar

### Identificación

| Campo                        | Detalle                      |
| ---------------------------- | ---------------------------- |
| **ID**                 | TP08                         |
| **Nombre**             | Rendir evaluación y aprobar |
| **Tipo**               | Manual                       |
| **Prioridad**          | Crítica                     |
| **Requisito cubierto** | RF16 (Evaluaciones)          |

### Precondiciones

- Estudiante inscrito en el curso.
- Quiz activo con preguntas y respuestas.
- El estudiante NO tiene intento activo previo.

### Pasos de ejecución

| # | Acción                       | Resultado esperado                    |
| - | ----------------------------- | ------------------------------------- |
| 1 | Login como estudiante         | Redirige a "Mis cursos"               |
| 2 | Navegar al módulo con quiz   | Se muestra el módulo                 |
| 3 | Click en "Rendir evaluación" | Se carga el formulario                |
| 4 | Responder todas correctamente | Se marcan las opciones                |
| 5 | Click en "Enviar respuestas"  | Se procesa el POST                    |
| 6 | Verificar puntaje             | Score = 100%                          |
| 7 | Verificar mensaje             | "¡Felicitaciones! Aprobaste el quiz" |

### Resultado esperado

El quiz se procesa, se calcula 100% y se marca como aprobado.

### Resultado obtenido

| Campo          | Detalle             |
| -------------- | ------------------- |
| Estado         | ⬜ PASA  ⬜ FALLA   |
| Score obtenido | ____%               |
| Observaciones  |                     |
| Evidencia      | Captura de pantalla |

---

## TP09 — Rendir evaluación y reprobar

### Identificación

| Campo                        | Detalle                       |
| ---------------------------- | ----------------------------- |
| **ID**                 | TP09                          |
| **Nombre**             | Rendir evaluación y reprobar |
| **Tipo**               | Manual                        |
| **Prioridad**          | Crítica                      |
| **Requisito cubierto** | RF16 (Evaluaciones)           |

### Precondiciones

- Estudiante inscrito.
- Quiz activo con `passing_score = 70`.

### Pasos de ejecución

| # | Acción                       | Resultado esperado                      |
| - | ----------------------------- | --------------------------------------- |
| 1 | Login como estudiante         | Redirige a "Mis cursos"                 |
| 2 | Navegar al módulo con quiz   | Se muestra el módulo                   |
| 3 | Click en "Rendir evaluación" | Se carga el formulario                  |
| 4 | Responder incorrectamente     | Se marcan opciones erróneas            |
| 5 | Click en "Enviar respuestas"  | Se procesa el POST                      |
| 6 | Verificar puntaje             | Score < 70%                             |
| 7 | Verificar mensaje             | "No aprobaste el quiz. Obtuviste un X%" |

### Resultado esperado

El quiz se procesa, se marca como reprobado y se muestra advertencia.

### Resultado obtenido

| Campo          | Detalle             |
| -------------- | ------------------- |
| Estado         | ⬜ PASA  ⬜ FALLA   |
| Score obtenido | ____%               |
| Observaciones  |                     |
| Evidencia      | Captura de pantalla |

---

## TP10 — Ver resultado detallado de una evaluación

### Identificación

| Campo                        | Detalle                          |
| ---------------------------- | -------------------------------- |
| **ID**                 | TP10                             |
| **Nombre**             | Ver resultado detallado del quiz |
| **Tipo**               | Manual                           |
| **Prioridad**          | Media                            |
| **Requisito cubierto** | RF16 (Evaluaciones)              |

### Precondiciones

- Estudiante con al menos un intento completado.

### Pasos de ejecución

| # | Acción                             | Resultado esperado                             |
| - | ----------------------------------- | ---------------------------------------------- |
| 1 | Login como estudiante               | Redirige a "Mis cursos"                        |
| 2 | Navegar al curso con intento previo | Detalle del curso                              |
| 3 | Click en "Ver resultado"            | Se muestra página de resultado                |
| 4 | Verificar puntaje mostrado          | Coincide con el obtenido                       |
| 5 | Verificar listado de preguntas      | Aparecen todas las preguntas                   |
| 6 | Verificar respuestas marcadas       | Se indica la opción elegida y si fue correcta |

### Resultado esperado

El estudiante puede revisar el detalle de su intento, viendo aciertos y errores.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP11 — Crear curso como instructor

### Identificación

| Campo                        | Detalle                                       |
| ---------------------------- | --------------------------------------------- |
| **ID**                 | TP11                                          |
| **Nombre**             | Creación de curso por instructor             |
| **Tipo**               | Manual                                        |
| **Prioridad**          | Alta                                          |
| **Requisito cubierto** | RF02 (Gestión de cursos), RF12 (Crear curso) |

### Precondiciones

- Instructor autenticado (`is_staff=True`, en grupo Instructores).
- Existe al menos una materia (`Subject`).

### Pasos de ejecución

| # | Acción                                     | Resultado esperado                  |
| - | ------------------------------------------- | ----------------------------------- |
| 1 | Login como instructor                       | Redirige al CMS (`/course/mine/`) |
| 2 | Click en "Crear curso"                      | Se muestra formulario               |
| 3 | Completar: materia, título, slug, overview | Campos aceptados                    |
| 4 | Click en "Guardar"                          | Se crea el curso                    |
| 5 | Verificar listado CMS                       | El nuevo curso aparece en la lista  |
| 6 | Verificar`owner`                          | El curso pertenece al instructor    |

### Resultado esperado

El instructor crea un curso que queda asociado a su cuenta.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP12 — Agregar contenido polimórfico

### Identificación

| Campo                        | Detalle                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| **ID**                 | TP12                                                       |
| **Nombre**             | Agregar los 4 tipos de contenido                           |
| **Tipo**               | Manual                                                     |
| **Prioridad**          | Alta                                                       |
| **Requisito cubierto** | RF04 (Gestión de contenidos), RF09 (Admin. de contenidos) |

### Precondiciones

- Instructor autenticado.
- Curso creado con al menos un módulo.

### Pasos de ejecución

| # | Acción                                | Resultado esperado                 |
| - | -------------------------------------- | ---------------------------------- |
| 1 | Ir al CMS y abrir un curso             | Detalle de módulos                |
| 2 | Click en "Editar módulos"             | Formulario de módulos             |
| 3 | Ir a un módulo → "Agregar contenido" | Se listan 4 tipos                  |
| 4 | Agregar**Texto**                 | Se crea`Text` + `Content`      |
| 5 | Agregar**Imagen**                | Se crea`Image` + `Content`     |
| 6 | Agregar**Video** (URL YouTube)   | Se crea`Video` + `Content`     |
| 7 | Agregar**Archivo** (PDF)         | Se crea`File` + `Content`      |
| 8 | Verificar en el curso                  | Los 4 contenidos aparecen en orden |

### Resultado esperado

Se crean los 4 tipos de contenido polimórfico sin conflictos.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP13 — Reordenar módulos y contenidos (Drag & Drop)

### Identificación

| Campo                        | Detalle                             |
| ---------------------------- | ----------------------------------- |
| **ID**                 | TP13                                |
| **Nombre**             | Reordenar módulos y contenidos     |
| **Tipo**               | Manual                              |
| **Prioridad**          | Media                               |
| **Requisito cubierto** | RF10 (Reordenamiento de contenidos) |

### Precondiciones

- Instructor autenticado.
- Curso con al menos 2 módulos y 2 contenidos en un módulo.

### Pasos de ejecución

| # | Acción                               | Resultado esperado                   |
| - | ------------------------------------- | ------------------------------------ |
| 1 | Ir al CMS y abrir un curso            | Lista de módulos                    |
| 2 | Arrastrar un módulo a otra posición | Se actualiza el orden visual         |
| 3 | Verificar que se guarda               | Al recargar, mantiene el nuevo orden |
| 4 | Ir a un módulo con contenidos        | Lista de contenidos                  |
| 5 | Arrastrar un contenido                | Se reordena                          |
| 6 | Recargar la página                   | El orden se mantiene                 |

### Resultado esperado

El drag & drop funciona y persiste el orden en la base de datos.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP14 — Visualización del Dashboard de KPIs

### Identificación

| Campo                        | Detalle                                |
| ---------------------------- | -------------------------------------- |
| **ID**                 | TP14                                   |
| **Nombre**             | Dashboard de KPIs para Superintendente |
| **Tipo**               | Manual                                 |
| **Prioridad**          | Alta                                   |
| **Requisito cubierto** | RF11 (Dashboard de KPIs)               |

### Precondiciones

- Superusuario autenticado.
- Existen cursos, estudiantes inscritos e intentos de evaluación.

### Pasos de ejecución

| # | Acción                                 | Resultado esperado                    |
| - | --------------------------------------- | ------------------------------------- |
| 1 | Login como superusuario                 | Redirige al admin                     |
| 2 | Ir a`/admin/dashboard-kpis/`          | Se muestra el dashboard               |
| 3 | Verificar KPI "Total Alumnos Inscritos" | Número correcto                      |
| 4 | Verificar KPI "Alumnos que Finalizaron" | Número correcto                      |
| 5 | Verificar KPI "Promedio de Notas"       | Porcentaje con 1 decimal              |
| 6 | Verificar KPI "Demora Promedio"         | Días con indicador verde/rojo        |
| 7 | Verificar tabla "Detalle por Curso"     | Aparecen los cursos con sus métricas |
| 8 | Verificar badge de umbral               | Verde si cumple meta, rojo si no      |

### Resultado esperado

El dashboard muestra KPIs reales, con indicadores de color según umbrales.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## TP15 — Aislamiento de datos entre instructores

### Identificación

| Campo                        | Detalle                                             |
| ---------------------------- | --------------------------------------------------- |
| **ID**                 | TP15                                                |
| **Nombre**             | Aislamiento de datos entre instructores             |
| **Tipo**               | Manual                                              |
| **Prioridad**          | Crítica                                            |
| **Requisito cubierto** | RF05 (Control de acceso), RNF05 (Seguridad backend) |

### Precondiciones

- Existen 2 instructores: Instructor A e Instructor B.
- Cada uno tiene al menos un curso propio.
- Ambos tienen permisos de admin.

### Pasos de ejecución

| # | Acción                                                                 | Resultado esperado              |
| - | ----------------------------------------------------------------------- | ------------------------------- |
| 1 | Login como Instructor A                                                 | Redirige al CMS                 |
| 2 | Ir a`/course/mine/`                                                   | Solo se ven los cursos de A     |
| 3 | Verificar que NO aparece el curso de B                                  | Curso de B oculto               |
| 4 | Ir al admin:`/admin/courses/course/`                                  | Solo aparecen cursos de A       |
| 5 | Ir a`/admin/courses/question/`                                        | Solo preguntas de cursos de A   |
| 6 | Ir a`/admin/courses/quiz/`                                            | Solo quizzes de cursos de A     |
| 7 | Intentar acceder a URL directa de curso de B (`/course/<id_B>/edit/`) | Recibe 403/404                  |
| 8 | Login como Instructor B y repetir                                       | Mismo comportamiento simétrico |

### Resultado esperado

Cada instructor solo ve y gestiona sus propios datos. No hay filtración cruzada.

### Resultado obtenido

| Campo         | Detalle             |
| ------------- | ------------------- |
| Estado        | ⬜ PASA  ⬜ FALLA   |
| Observaciones |                     |
| Evidencia     | Captura de pantalla |

---

## Resumen de ejecución

| ID   | Caso                           | Estado | Fecha | Responsable |
| ---- | ------------------------------ | ------ | ----- | ----------- |
| TP01 | Registro de estudiante         | ⬜     |       |             |
| TP02 | Login válido                  | ⬜     |       |             |
| TP03 | Login inválido                | ⬜     |       |             |
| TP04 | Cierre de sesión              | ⬜     |       |             |
| TP05 | Catálogo de cursos            | ⬜     |       |             |
| TP06 | Inscripción a curso           | ⬜     |       |             |
| TP07 | Visualización de contenidos   | ⬜     |       |             |
| TP08 | Rendir quiz y aprobar          | ⬜     |       |             |
| TP09 | Rendir quiz y reprobar         | ⬜     |       |             |
| TP10 | Ver resultado detallado        | ⬜     |       |             |
| TP11 | Crear curso (instructor)       | ⬜     |       |             |
| TP12 | Agregar contenido polimórfico | ⬜     |       |             |
| TP13 | Reordenar módulos/contenidos  | ⬜     |       |             |
| TP14 | Dashboard de KPIs              | ⬜     |       |             |
| TP15 | Aislamiento entre instructores | ⬜     |       |             |

**Total**: 15 casos
**PASAN**: ____ / 15
**FALLAN**: ____ / 15
**Observaciones generales**: _______________________________________________

---

## Trazabilidad con Requisitos Funcionales

| TP                     | Requisito Cubierto                        |
| ---------------------- | ----------------------------------------- |
| TP01, TP02, TP03, TP04 | RF01 (Autenticación)                     |
| TP05                   | RF06 (Catálogo)                          |
| TP06                   | RF07 (Inscripción)                       |
| TP07                   | RF08 (Visualización de lecciones)        |
| TP08, TP09, TP10       | RF16 (Evaluaciones)                       |
| TP11                   | RF02, RF12 (Gestión/Creación de cursos) |
| TP12                   | RF04, RF09 (Gestión de contenidos)       |
| TP13                   | RF10 (Reordenamiento)                     |
| TP14                   | RF11 (Dashboard de KPIs)                  |
| TP15                   | RF05, RNF05 (Control de acceso)           |

**Cobertura**: 15 pruebas manuales cubren **11 de 17 RF** (65%) adicionales a las
**42 pruebas automatizadas** que cubren el resto.

---

## Conclusión

Las 15 pruebas manuales complementan la suite automatizada y validan los
flujos críticos de usuario en el navegador. Los resultados deben registrarse
al final del Sprint para consolidar la evidencia de calidad del sistema.
