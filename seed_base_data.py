"""
Script de carga de datos BASE para Bomberos Educa
Solo crea: Materias, Grupos y Usuarios
Los cursos, módulos y videos se crearán manualmente para el manual de instructores.

Ejecutar con: python manage.py shell < seed_base_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educa.settings')
django.setup()

from django.contrib.auth.models import User, Group
from courses.models import Subject

print("=" * 60)
print("🚒 CARGA DE DATOS BASE - BOMBEROS EDUCA")
print("=" * 60)

# ============================================
# 1. CREAR MATERIAS (SUBJECTS)
# ============================================
print("\n📚 Creando materias...")

materias_data = [
    {'title': 'Flota Vehicular', 'slug': 'flota-vehicular'},
    {'title': 'Protección Respiratoria', 'slug': 'proteccion-respiratoria'},
    {'title': 'Atención Prehospitalaria', 'slug': 'atencion-prehospitalaria'},
    {'title': 'Rescate Técnico', 'slug': 'rescate-tecnico'},
]

for data in materias_data:
    materia, created = Subject.objects.get_or_create(
        slug=data['slug'],
        defaults={'title': data['title']}
    )
    status = "✅ Creada" if created else "⚠️ Ya existía"
    print(f"  {status}: {materia.title}")

# ============================================
# 2. CREAR GRUPOS
# ============================================
print("\n👥 Creando grupos...")

grupos_data = ['Instructores', 'Estudiantes']
for nombre in grupos_data:
    grupo, created = Group.objects.get_or_create(name=nombre)
    status = "✅ Creado" if created else "⚠️ Ya existía"
    print(f"  {status}: {grupo.name}")

# ============================================
# 3. CREAR USUARIOS
# ============================================
print("\n👤 Creando usuarios...")

usuarios_data = [
    {
        'username': 'capitan_rojas',
        'password': 'bomberos2024',
        'first_name': 'Rodrigo',
        'last_name': 'Rojas',
        'email': 'r.rojas@bomberos.cl',
        'is_staff': True,
        'group': 'Instructores'
    },
    {
        'username': 'bombero_silva',
        'password': 'bomberos2024',
        'first_name': 'Carlos',
        'last_name': 'Silva',
        'email': 'c.silva@bomberos.cl',
        'is_staff': False,
        'group': 'Estudiantes'
    },
    {
        'username': 'bombera_fuentes',
        'password': 'bomberos2024',
        'first_name': 'Andrea',
        'last_name': 'Fuentes',
        'email': 'a.fuentes@bomberos.cl',
        'is_staff': False,
        'group': 'Estudiantes'
    },
]

for data in usuarios_data:
    if User.objects.filter(username=data['username']).exists():
        usuario = User.objects.get(username=data['username'])
        print(f"  ⚠️ Ya existía: {usuario.username}")
    else:
        usuario = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            is_staff=data['is_staff']
        )
        grupo = Group.objects.get(name=data['group'])
        usuario.groups.add(grupo)
        print(f"  ✅ Creado: {usuario.username} ({data['group']})")

# ============================================
# RESUMEN FINAL
# ============================================
print("\n" + "=" * 60)
print("📊 RESUMEN DE CARGA BASE")
print("=" * 60)
print(f"  ✅ Materias creadas: {Subject.objects.count()}")
print(f"  ✅ Grupos creados: {Group.objects.filter(name__in=['Instructores', 'Estudiantes']).count()}")
print(f"  ✅ Usuarios creados: {User.objects.exclude(username='admin').count()}")
print("\n⚠️  PENDIENTE PARA CARGA MANUAL (para el manual de instructores):")
print("  📖 Cursos")
print("  📚 Módulos")
print("  🎬 Videos")
print("  📝 Quizzes y preguntas")
print("=" * 60)
print("\n🎉 ¡Carga base completada!")
print("\n📋 Próximos pasos:")
print("  1. Inicia sesión como 'capitan_rojas' en /accounts/login/")
print("  2. Ve a /course/ para crear cursos manualmente")
print("  3. Toma capturas de pantalla para el manual")
print("=" * 60)