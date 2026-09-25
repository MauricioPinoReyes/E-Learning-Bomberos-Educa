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


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


# ============================================
# ADMIN DE EVALUACIONES (QUIZZES)
# ============================================

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'order', 'points']
    list_filter = ['quiz']
    inlines = [AnswerInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'passing_score', 'is_active', 'created']
    list_filter = ['is_active', 'module__course']
    search_fields = ['title', 'module__title']
    inlines = [QuestionInline]


# SOLO UN REGISTRO DE QuizAttempt (con inline de StudentAnswer)
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