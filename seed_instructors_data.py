"""
Script para poblar la BD con datos de dos instructores, sus cursos, modulos, 
contenidos (videos) y evaluaciones (quizzes con preguntas).
Ejecutar con: cmd /c "python manage.py shell < seed_instructors_data.py"
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educa.settings')
django.setup()

from django.contrib.auth.models import User, Group
from courses.models import Subject, Course, Module, Content, Video, Quiz, Question, Answer

print("=" * 60)
print("POBLANDO DATOS PARA DOS INSTRUCTORES")
print("=" * 60)

# ============================================
# 1. PREPARAR USUARIOS Y GRUPOS
# ============================================
print("\nConfigurando Instructores...")

grupo_instructores, _ = Group.objects.get_or_create(name='Instructores')

instructor1, _ = User.objects.get_or_create(
    username='capitan_rojas',
    defaults={
        'first_name': 'Rodrigo',
        'last_name': 'Rojas',
        'email': 'r.rojas@bomberos.cl',
        'is_staff': True
    }
)
instructor1.set_password('bomberos2024')
instructor1.save()
instructor1.groups.add(grupo_instructores)

instructor2, created2 = User.objects.get_or_create(
    username='teniente_mendez',
    defaults={
        'first_name': 'Laura',
        'last_name': 'Mendez',
        'email': 'l.mendez@bomberos.cl',
        'is_staff': True
    }
)
if created2:
    instructor2.set_password('bomberos2024')
    instructor2.save()
    instructor2.groups.add(grupo_instructores)
    print(f"  Creada: {instructor2.get_full_name()}")
else:
    print(f"  Ya existia: {instructor2.get_full_name()}")

# ============================================
# 2. OBTENER MATERIAS
# ============================================
print("\nObteniendo materias...")
materia_flota = Subject.objects.get(slug='flota-vehicular')
materia_rescate = Subject.objects.get(slug='rescate-tecnico')
materia_era = Subject.objects.get(slug='proteccion-respiratoria')
materia_aph = Subject.objects.get(slug='atencion-prehospitalaria')

# ============================================
# 3. FUNCIONES AUXILIARES
# ============================================
def crear_video(owner, titulo, url):
    video, _ = Video.objects.get_or_create(owner=owner, title=titulo, defaults={'url': url})
    return video

def crear_contenido(modulo, item, orden):
    from django.contrib.contenttypes.models import ContentType
    ct = ContentType.objects.get_for_model(item)
    Content.objects.get_or_create(
        module=modulo, content_type=ct, object_id=item.id,
        defaults={'order': orden}
    )

def crear_quiz_y_preguntas(modulo, titulo, preguntas_data):
    quiz, _ = Quiz.objects.get_or_create(
        module=modulo,
        defaults={
            'title': titulo,
            'description': f'Evaluacion de {modulo.title}',
            'passing_score': 70,
            'time_limit': 30,
            'is_active': True
        }
    )
    for i, p_data in enumerate(preguntas_data):
        q, _ = Question.objects.get_or_create(
            quiz=quiz, text=p_data['text'],
            defaults={'order': i, 'points': 10}
        )
        for j, r_text in enumerate(p_data['respuestas']):
            es_correcta = (r_text == p_data['correcta'])
            Answer.objects.get_or_create(
                question=q, text=r_text,
                defaults={'order': j, 'is_correct': es_correcta}
            )

# ============================================
# 4. DATOS DEL INSTRUCTOR 1 (CAPITAN ROJAS)
# ============================================
print("\nCargando datos para Capitan Rojas...")

curso1, _ = Course.objects.get_or_create(
    slug='unidades-ataque-abastecimiento',
    defaults={
        'owner': instructor1, 'subject': materia_flota,
        'title': 'Unidades de Ataque y Abastecimiento',
        'overview': 'Operacion de unidades forestales, cisternas y equipos de bombeo.'
    }
)

mod1_1, _ = Module.objects.get_or_create(course=curso1, title='Unidades Forestales y Estructurales', defaults={'order': 0})
vid1 = crear_video(instructor1, 'Academia BF-1', 'https://www.youtube.com/watch?v=BF1_EXAMPLE')
crear_contenido(mod1_1, vid1, 0)
crear_quiz_y_preguntas(mod1_1, 'Quiz: Unidades Forestales', [
    {'text': 'Cual es la funcion principal de la unidad BF-1?', 'respuestas': ['Combate forestal', 'Rescate acuatico', 'Atencion medica'], 'correcta': 'Combate forestal'},
    {'text': 'Que tipo de mangueras usa principalmente?', 'respuestas': ['38mm y 50mm', '100mm', 'No usa mangueras'], 'correcta': '38mm y 50mm'},
    {'text': 'Cuantos tripulantes requiere minimo?', 'respuestas': ['2', '4', '6'], 'correcta': '4'}
])

mod1_2, _ = Module.objects.get_or_create(course=curso1, title='Unidades Cisterna y Equipos de Bombeo', defaults={'order': 1})
vid2 = crear_video(instructor1, 'Academia Z-1', 'https://www.youtube.com/watch?v=Z1_EXAMPLE')
vid3 = crear_video(instructor1, 'Funcionamiento de Motobombas', 'https://www.youtube.com/watch?v=MOTO_EXAMPLE')
crear_contenido(mod1_2, vid2, 0)
crear_contenido(mod1_2, vid3, 1)

curso2, _ = Course.objects.get_or_create(
    slug='desencarcelacion-vehicular',
    defaults={
        'owner': instructor1, 'subject': materia_rescate,
        'title': 'Desencarcelacion Vehicular',
        'overview': 'Uso de herramientas hidraulicas para rescate en accidentes de transito.'
    }
)
mod2_1, _ = Module.objects.get_or_create(course=curso2, title='Herramientas Hidraulicas', defaults={'order': 0})
vid4 = crear_video(instructor1, 'Equipo Lukas', 'https://www.youtube.com/watch?v=LUKAS_EXAMPLE')
crear_contenido(mod2_1, vid4, 0)
crear_quiz_y_preguntas(mod2_1, 'Quiz: Herramientas Hidraulicas', [
    {'text': 'Que presion maxima suele manejar el equipo Lukas?', 'respuestas': ['720 bar', '100 bar', '50 bar'], 'correcta': '720 bar'},
    {'text': 'Cual es la herramienta de corte llamada?', 'respuestas': ['Cizalla', 'Martillo', 'Palanca'], 'correcta': 'Cizalla'},
    {'text': 'Que fluido utilizan?', 'respuestas': ['Aceite hidraulico', 'Agua', 'Aire comprimido'], 'correcta': 'Aceite hidraulico'}
])

# ============================================
# 5. DATOS DEL INSTRUCTOR 2 (TENIENTE MENDEZ)
# ============================================
print("\nCargando datos para Teniente Mendez...")

curso3, _ = Course.objects.get_or_create(
    slug='operacion-mantenimiento-era',
    defaults={
        'owner': instructor2, 'subject': materia_era,
        'title': 'Operacion y Mantenimiento de Equipos ERA',
        'overview': 'Uso correcto y mantenimiento de equipos de respiracion autonoma.'
    }
)
mod3_1, _ = Module.objects.get_or_create(course=curso3, title='Uso y Colocacion del Equipo', defaults={'order': 0})
vid5 = crear_video(instructor2, 'Equipos ERA', 'https://www.youtube.com/watch?v=ERA_EXAMPLE')
crear_contenido(mod3_1, vid5, 0)
crear_quiz_y_preguntas(mod3_1, 'Quiz: Uso de ERA', [
    {'text': 'Que significa ERA?', 'respuestas': ['Equipo de Respiracion Autonoma', 'Equipo de Rescate Aereo', 'Ninguna'], 'correcta': 'Equipo de Respiracion Autonoma'},
    {'text': 'Cual es la presion estandar de un cilindro?', 'respuestas': ['3000 PSI', '100 PSI', '10 PSI'], 'correcta': '3000 PSI'},
    {'text': 'Que indica la alarma del equipo?', 'respuestas': ['Baja presion', 'Fuga de aire', 'Bateria baja'], 'correcta': 'Baja presion'}
])

mod3_2, _ = Module.objects.get_or_create(course=curso3, title='Inspeccion y Decontaminacion', defaults={'order': 1})
vid6 = crear_video(instructor2, 'Mantenimiento de ERA', 'https://www.youtube.com/watch?v=MANT_ERA_EXAMPLE')
crear_contenido(mod3_2, vid6, 0)

curso4, _ = Course.objects.get_or_create(
    slug='soporte-vital-basico',
    defaults={
        'owner': instructor2, 'subject': materia_aph,
        'title': 'Soporte Vital Basico',
        'overview': 'Protocolos de RCP, uso de DEA y manejo inicial de trauma.'
    }
)
mod4_1, _ = Module.objects.get_or_create(course=curso4, title='Reanimacion Cardiopulmonar', defaults={'order': 0})
vid7 = crear_video(instructor2, 'RCP + DEA', 'https://www.youtube.com/watch?v=RCP_EXAMPLE')
crear_contenido(mod4_1, vid7, 0)
crear_quiz_y_preguntas(mod4_1, 'Quiz: RCP y DEA', [
    {'text': 'Cual es el ritmo de compresiones por minuto?', 'respuestas': ['100-120', '60-80', '150'], 'correcta': '100-120'},
    {'text': 'Que significa DEA?', 'respuestas': ['Desfibrilador Externo Automatico', 'Dispositivo de Emergencia Avanzada', 'Ninguna'], 'correcta': 'Desfibrilador Externo Automatico'},
    {'text': 'Cual es la relacion compresion/ventilacion en adultos?', 'respuestas': ['30:2', '15:2', '10:1'], 'correcta': '30:2'}
])

mod4_2, _ = Module.objects.get_or_create(course=curso4, title='Monitoreo Fisiologico', defaults={'order': 1})
vid8 = crear_video(instructor2, 'Monitores de Signos Vitales', 'https://www.youtube.com/watch?v=MONITOR_EXAMPLE')
crear_contenido(mod4_2, vid8, 0)

# ============================================
# RESUMEN FINAL
# ============================================
print("\n" + "=" * 60)
print("RESUMEN DE POBLADO")
print("=" * 60)
print(f"  Capitan {instructor1.get_full_name()}: {Course.objects.filter(owner=instructor1).count()} cursos")
print(f"  Teniente {instructor2.get_full_name()}: {Course.objects.filter(owner=instructor2).count()} cursos")
print(f"  Total Modulos: {Module.objects.count()}")
print(f"  Total Videos: {Video.objects.count()}")
print(f"  Total Quizzes: {Quiz.objects.count()}")
print(f"  Total Preguntas: {Question.objects.count()}")
print("=" * 60)
print("\nBase de datos lista para la demo de dos instructores!")
print("\nProximos pasos:")
print("  1. Inicia sesion como 'capitan_rojas' y verifica que SOLO ve sus 2 cursos.")
print("  2. Inicia sesion como 'teniente_mendez' y verifica que SOLO ve sus 2 cursos.")
print("  3. Entra como 'admin' al dashboard y veras metricas combinadas.")
print("=" * 60)