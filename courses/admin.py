from django.contrib import admin
from .models import Subject, Course, Module
from .models import Quiz, Question, Answer, QuizAttempt, StudentAnswer


# ============================================
# ADMIN DE MATERIAS Y CURSOS
# ============================================

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    # Las Materias son globales, todos los instructores deben verlas.


class ModuleInline(admin.StackedInline):
    model = Module
    
    # 🔒 FILTRAR MÓDULOS: Solo ver módulos de sus propios cursos
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__owner=request.user)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

    #FILTRAR CURSOS: Solo ver sus propios cursos
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Si es instructor, filtrar por el owner (el usuario logueado)
        return qs.filter(owner=request.user)

    # Traducción de headers
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        # Los verbose_name se toman automáticamente del modelo
        return list_display
    
    # Asegurar que se usen los verbose_name del modelo
    list_display_links = ['title']
    


# ============================================
# ADMIN DE EVALUACIONES (QUIZZES)
# ============================================

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # MEJORA UX (Obs 3): Mostramos el Curso, texto corto y validación visual
    list_display = ['short_text', 'quiz_course', 'quiz', 'order', 'points', 'has_correct_answer']
    list_filter = ['quiz__module__course__title', 'quiz'] # Filtrar por Curso
    search_fields = ['text']
    inlines = [AnswerInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(quiz__module__course__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # MEJORA UX (Obs 3): El instructor solo ve sus propios quizzes en el desplegable
        if db_field.name == "quiz":
            kwargs["queryset"] = Quiz.objects.filter(module__course__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Métodos auxiliares para mejorar la vista de lista
    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Pregunta'

    def quiz_course(self, obj):
        return obj.quiz.module.course.title
    quiz_course.short_description = 'Curso'

    def has_correct_answer(self, obj):
        count = obj.answers.filter(is_correct=True).count()
        if count == 1: return '✅ Sí'
        if count == 0: return '❌ No'
        return f'⚠️ {count} (Múltiples)'
    has_correct_answer.short_description = 'Resp. Correcta'


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'passing_score', 'is_active']
    list_filter = ['is_active', 'module__course']
    search_fields = ['title', 'module__title']  
    inlines = [QuestionInline] 
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(module__course__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "module":
            kwargs["queryset"] = Module.objects.filter(course__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# CORRECCIÓN CRÍTICA: Movido ANTES de QuizAttemptAdmin para evitar NameError
class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ['question', 'selected_answer']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'passed', 'started_at', 'completed_at']
    list_filter = ['passed', 'quiz', 'started_at']
    search_fields = ['student__username', 'quiz__title']
    readonly_fields = ['student', 'quiz', 'score', 'passed', 'started_at', 'completed_at']
    inlines = [StudentAnswerInline]

    # SOLUCIÓN OBSERVACIÓN 2 (Seguridad):
    def has_add_permission(self, request):
        # Prohibido crear intentos manualmente. Deben generarse desde la web.
        return False

    def has_change_permission(self, request, obj=None):
        # Prohibido modificar notas o estados manualmente.
        return False

    def has_delete_permission(self, request, obj=None):
        # Solo el superusuario puede borrar intentos en casos de emergencia.
        return request.user.is_superuser