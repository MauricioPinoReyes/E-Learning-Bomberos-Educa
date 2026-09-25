from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from courses.models import Quiz, QuizAttempt, StudentAnswer


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
        username=cd['username'], password=cd['password1']
        )
        login(self.request, user)
        return result

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'student_course_detail', args=[self.course.id]
        )
    

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course    
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()

        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # get first module
            #context['module'] = course.modules.all()[0]
            # cambiada por la funcion first(), para el caso que no hayan cursos sin modulo
            context['module'] = course.modules.all().first()
        return context
    

@login_required
def quiz_take_view(request, quiz_id):
    """Vista para que el bombero rinda el quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Verificar si el bombero está inscrito en el curso
    course = quiz.module.course
    if request.user not in course.students.all():
        messages.error(request, 'Debes estar inscrito en el curso para rendir esta evaluación.')
        return redirect('student_course_list')
    
    # Verificar si ya existe un intento en progreso
    attempt = QuizAttempt.objects.filter(
        student=request.user,
        quiz=quiz,
        completed_at__isnull=True
    ).first()
    
    # Si no hay intento, crear uno nuevo
    if not attempt:
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz
        )
    
    # Obtener todas las preguntas del quiz
    questions = quiz.questions.all().prefetch_related('answers')
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'questions': questions,
    }
    
    return render(request, 'students/quiz/take.html', context)


@login_required
def quiz_submit_view(request, quiz_id):
    """Vista para procesar las respuestas del quiz"""
    if request.method != 'POST':
        return redirect('quiz_take', quiz_id=quiz_id)
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Obtener o crear el intento
    attempt = QuizAttempt.objects.filter(
        student=request.user,
        quiz=quiz,
        completed_at__isnull=True
    ).first()
    
    if not attempt:
        messages.error(request, 'No tienes un intento activo para este quiz.')
        return redirect('student_course_list')
    
    # Procesar las respuestas
    questions = quiz.questions.all()
    correct_count = 0
    total_points = 0
    
    for question in questions:
        answer_id = request.POST.get(f'question_{question.id}')
        
        if answer_id:
            try:
                selected_answer = question.answers.get(id=answer_id)
                
                # Guardar la respuesta del estudiante
                StudentAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={'selected_answer': selected_answer}
                )
                
                # Contar si es correcta
                if selected_answer.is_correct:
                    correct_count += 1
                    total_points += question.points
                    
            except question.answers.model.DoesNotExist:
                pass
    
    # Calcular el puntaje
    total_possible_points = sum(q.points for q in questions)
    if total_possible_points > 0:
        score = (total_points / total_possible_points) * 100
    else:
        score = 0
    
    # Actualizar el intento
    attempt.score = score
    attempt.passed = score >= quiz.passing_score
    attempt.completed_at = timezone.now()
    attempt.save()
    
    # Mensaje de resultado
    if attempt.passed:
        messages.success(request, f'¡Felicitaciones! Aprobaste el quiz con un {score:.1f}%.')
    else:
        messages.warning(request, f'No aprobaste el quiz. Obtuviste un {score:.1f}%. Necesitas al menos {quiz.passing_score}% para aprobar.')
    
    return redirect('quiz_result', quiz_id=quiz_id, attempt_id=attempt.id)


@login_required
def quiz_result_view(request, quiz_id, attempt_id):
    """Vista para mostrar el resultado del quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    # Obtener las respuestas del estudiante
    student_answers = attempt.answers.select_related('question', 'selected_answer').all()
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'student_answers': student_answers,
    }
    
    return render(request, 'students/quiz/result.html', context)
