from django.contrib.auth.models import User
from django.db import models
from .fields import OrderField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from django.utils import timezone

class Subject(models.Model):
    """Asignatura o materia (ej: Matemáticas, Programación, etc.)"""
    title = models.CharField('Título',max_length=200)
    slug = models.SlugField('Slug',max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'

    def __str__(self):
        return self.title


class Course(models.Model):
    """Curso creado por un instructor, perteneciente a una materia."""
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE,
        verbose_name='Materia'
    )
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True)
    overview = models.TextField('Descripción general')
    created = models.DateTimeField('Creado el', auto_now_add=True)

    students = models.ManyToManyField(
    User,
    related_name='courses_joined',
    blank=True
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.title


class Module(models.Model):
    """Módulo o unidad dentro de un curso."""
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE,
        verbose_name='Curso'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in':('text', 'video', 'image', 'file')
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id') 
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']
        verbose_name = 'Contenido'
        verbose_name_plural = 'Contenidos'


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = 'Elemento Base'
        verbose_name_plural = 'Elementos Base'

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
    )    

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()
    
    class Meta:
        verbose_name = 'Texto'
        verbose_name_plural = 'Textos'


class File(ItemBase):
    file = models.FileField(upload_to='files')

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'


class Image(ItemBase):
    file = models.FileField(upload_to='images')

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imágenes'


class Video(ItemBase):
    url = models.URLField()

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


class Quiz(models.Model):
    """Evaluación asociada a un módulo"""
    module = models.OneToOneField(
        Module, 
        on_delete=models.CASCADE, 
        related_name='quiz',
        verbose_name='Módulo'
    )
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción',blank=True)
    passing_score = models.IntegerField(
        default=70,
        help_text='Nota mínima para aprobar (0-100)',
        verbose_name='% Aprobación'
    )
    time_limit = models.IntegerField(
        null=True, 
        blank=True,
        help_text='Tiempo límite en minutos (opcional)'
    )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
    
    def __str__(self):
        return f'{self.title} - {self.module.title}'

    @property
    def owner(self):
        """El owner del quiz es el owner del curso"""
        return self.module.course.owner
    
    def get_total_questions(self):
        return self.questions.count()


class Question(models.Model):
    """Pregunta de opción múltiple"""
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='questions',
        verbose_name='Evaluación'
    )
    text = models.TextField(help_text='Texto de la pregunta')
    order = models.IntegerField('Orden',default=0)
    points = models.IntegerField('Puntos',default=1, help_text='Puntos que vale esta pregunta')
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
    
    def __str__(self):
        return f'Pregunta {self.order}: {self.text[:50]}...'


class Answer(models.Model):
    """Opción de respuesta para una pregunta"""
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='answers'
    )
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
    
    def __str__(self):
        return f'{self.text[:50]}... {"✓" if self.is_correct else "✗"}'


class QuizAttempt(models.Model):
    """Intento de un estudiante al resolver un quiz"""
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name='Estudiante'
    )
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Evaluación'
    )
    started_at = models.DateTimeField('inicio',auto_now_add=True)
    completed_at = models.DateTimeField('termino',null=True, blank=True)
    score = models.FloatField('puntaje',null=True, blank=True)
    passed = models.BooleanField('aprobado',default=False)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Intento de Evaluación'
        verbose_name_plural = 'Intentos de Evaluaciones'
    
    def __str__(self):
        status = '✓ Aprobado' if self.passed else '✗ Reprobado'
        return f'{self.student.username} - {self.quiz.title} ({status})'
    
    def calculate_score(self):
        """Calcula el puntaje del intento"""
        correct_answers = self.answers.filter(
            selected_answer__is_correct=True
        ).count()
        total_questions = self.quiz.questions.count()
        
        if total_questions == 0:
            return 0
        
        self.score = (correct_answers / total_questions) * 100
        self.passed = self.score >= self.quiz.passing_score
        self.completed_at = timezone.now()
        self.save()
        return self.score


    @property
    def threshold_color(self):
        """Devuelve el color del indicador según el resultado."""
        if self.score is None:
            return 'gray'
        return 'green' if self.passed else 'red'


class StudentAnswer(models.Model):
    """Respuesta individual de un estudiante a una pregunta"""
    attempt = models.ForeignKey(
        QuizAttempt, 
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE
    )
    selected_answer = models.ForeignKey(
        Answer, 
        on_delete=models.CASCADE
    )
    
    class Meta:
        unique_together = ['attempt', 'question']
        verbose_name = 'Respuesta del Estudiante'
        verbose_name_plural = 'Respuestas de Estudiantes'