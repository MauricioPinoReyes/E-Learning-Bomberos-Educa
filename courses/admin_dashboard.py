from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg
from django.contrib.auth.models import User

from courses.models import Course, QuizAttempt, Quiz


@staff_member_required
def dashboard_kpis_view(request):
    """Vista personalizada del Dashboard de KPIs con métricas avanzadas"""
    
    # ============================================
    # 1. Total de Alumnos Inscritos (Matrículas)
    # ============================================
    total_alumnos_inscritos = sum(course.students.count() for course in Course.objects.all())
    
    # ============================================
    # 2. Alumnos que Finalizaron (Aprobaron al menos un quiz)
    # ============================================
    alumnos_finalizados = User.objects.filter(
        quiz_attempts__passed=True
    ).distinct().count()
    
    total_estudiantes = User.objects.filter(is_staff=False).count()
    
    # ============================================
    # 3. Tiempo Promedio de Finalización (Inscripción -> Aprobación)
    # ============================================
    intentos_aprobados = QuizAttempt.objects.filter(passed=True).select_related('student')
    
    dias_demora = []
    for intento in intentos_aprobados:
        demora = intento.completed_at.date() - intento.student.date_joined.date()
        dias_demora.append(demora.days)
    
    promedio_dias = round(sum(dias_demora) / len(dias_demora), 1) if dias_demora else 0
        
    # ============================================
    # 4. Promedio de Notas (de los aprobados)
    # ============================================
    resultado_avg = QuizAttempt.objects.filter(passed=True).aggregate(Avg('score'))
    promedio_notas = round(resultado_avg['score__avg'] or 0, 1)
    
    # ============================================
    # Datos adicionales
    # ============================================
    total_intentos = QuizAttempt.objects.count()
    cursos_aprobados = QuizAttempt.objects.filter(passed=True).count()
    tasa_aprobacion = round((cursos_aprobados / total_intentos * 100), 1) if total_intentos > 0 else 0.0
    
    total_cursos = Course.objects.count()
    cursos_populares = Course.objects.annotate(num_students=Count('students')).order_by('-num_students')[:5]
    
    # ============================================
    # Definición de UMBRALES
    # ============================================
    UMBRAL_META_NOTA = 70.0
    UMBRAL_META_DIAS = 14  # Meta: terminar en menos de 14 días
    
    context = {
        'title': '📊 Dashboard de KPIs - Bomberos Educa',
        'total_alumnos_inscritos': total_alumnos_inscritos,
        'alumnos_finalizados': alumnos_finalizados,
        'total_estudiantes': total_estudiantes,
        'promedio_dias': promedio_dias,
        'promedio_notas': promedio_notas,
        'tasa_aprobacion': tasa_aprobacion,
        'total_cursos': total_cursos,
        'cursos_populares': cursos_populares,
        # Variables para los umbrales visuales
        'umbral_meta_nota': UMBRAL_META_NOTA,
        'umbral_meta_dias': UMBRAL_META_DIAS,
        'cumple_meta_notas': promedio_notas >= UMBRAL_META_NOTA,
        'cumple_meta_dias': promedio_dias <= UMBRAL_META_DIAS and promedio_dias > 0,
    }
    
    return render(request, 'admin/dashboard_kpis.html', context)


class DashboardAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard-kpis/', self.admin_view(dashboard_kpis_view), name='dashboard_kpis'),
        ]
        return custom_urls + urls