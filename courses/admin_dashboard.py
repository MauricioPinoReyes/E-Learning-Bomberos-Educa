from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Q
from django.contrib.auth.models import User

from courses.models import Course, QuizAttempt, Quiz

@staff_member_required
def dashboard_kpis_view(request):
    """Vista personalizada del Dashboard de KPIs con métricas reales y contexto"""
    
    # 1. Total de Alumnos Inscritos (Únicos, no suma duplicados si están en 2 cursos)
    total_alumnos_inscritos = User.objects.filter(
        courses_joined__isnull=False
    ).distinct().count()
    
    # 2. Alumnos que Finalizaron (Aprobaron al menos un quiz)
    alumnos_finalizados = User.objects.filter(
        quiz_attempts__passed=True
    ).distinct().count()
    
    # 3. Tiempo Promedio de Finalización
    intentos_aprobados = QuizAttempt.objects.filter(
        passed=True, completed_at__isnull=False
    ).select_related('student')
    
    dias_demora = []
    for intento in intentos_aprobados:
        if intento.student.date_joined and intento.completed_at:
            demora = (intento.completed_at - intento.student.date_joined).days
            if demora >= 0:
                dias_demora.append(demora)
    
    promedio_dias = round(sum(dias_demora) / len(dias_demora), 1) if dias_demora else 0
    
    # 4. Promedio de Notas (DE TODOS LOS INTENTOS FINALIZADOS, no solo aprobados)
    resultado_avg = QuizAttempt.objects.filter(
        completed_at__isnull=False
    ).aggregate(Avg('score'))
    promedio_notas = round(resultado_avg['score__avg'] or 0, 1)
    
    # 5. Tasa de Aprobación Real
    total_intentos = QuizAttempt.objects.filter(completed_at__isnull=False).count()
    intentos_aprobados_count = QuizAttempt.objects.filter(passed=True).count()
    tasa_aprobacion = round((intentos_aprobados_count / total_intentos * 100), 1) if total_intentos > 0 else 0.0
    
    # 6. Datos para el "Detalle por Curso" (El contexto que faltaba)
    cursos_detalle = Course.objects.annotate(
        total_inscritos=Count('students', distinct=True),
        total_aprobados=Count('students__quiz_attempts', filter=Q(students__quiz_attempts__passed=True), distinct=True),
        promedio_nota=Avg('students__quiz_attempts__score', filter=Q(students__quiz_attempts__completed_at__isnull=False))
    ).order_by('-total_inscritos')

    # UMBRALES
    UMBRAL_META_NOTA = 70.0
    UMBRAL_META_DIAS = 14
    
    context = {
        'title': ' Dashboard de KPIs - Bomberos Educa',
        'total_alumnos_inscritos': total_alumnos_inscritos,
        'alumnos_finalizados': alumnos_finalizados,
        'total_cursos': Course.objects.count(), # Reemplaza a total_estudiantes
        'promedio_dias': promedio_dias,
        'promedio_notas': promedio_notas,
        'tasa_aprobacion': tasa_aprobacion,
        'cursos_detalle': cursos_detalle, # Nuevo contexto
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