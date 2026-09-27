"""
Suite de tests para la plataforma Bomberos Educa.
Cubre: unitarias, integración, seguridad y flujo completo.

Ejecutar con:
    python manage.py test courses -v 2
    
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils import timezone

from courses.models import (
    Subject, Course, Module, Content, Text, Image, File, Video,
    Quiz, Question, Answer, QuizAttempt, StudentAnswer
)


# ============================================================
# TP01 - LOGIN VÁLIDO → SMART REDIRECT
# ============================================================
class LoginValidCredentialsTest(TestCase):
    """TP01: Login con credenciales válidas autentica y redirige."""

    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user('student', password='correctpass123')

    def test_login_stores_session(self):
        client = Client()
        response = client.post('/accounts/login/', {
            'username': 'student',
            'password': 'correctpass123'
        })
        self.assertEqual(response.status_code, 302,
                         f"Login falló. Status: {response.status_code}")
        self.assertIn('_auth_user_id', client.session)

    def test_login_redirects_to_smart_redirect(self):
        client = Client()
        response = client.post('/accounts/login/', {
            'username': 'student',
            'password': 'correctpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('smart_login_redirect'))


# ============================================================
# TP02 - LOGIN INVÁLIDO → ERROR
# ============================================================
class LoginInvalidCredentialsTest(TestCase):
    """TP02: Login con credenciales inválidas no autentica."""

    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user('student', password='correctpass123')

    def test_wrong_password_does_not_authenticate(self):
        client = Client()
        client.post('/accounts/login/', {
            'username': 'student',
            'password': 'wrongpass'
        })
        self.assertNotIn('_auth_user_id', client.session)

    def test_nonexistent_user_does_not_authenticate(self):
        client = Client()
        client.post('/accounts/login/', {
            'username': 'noexiste',
            'password': 'cualquiera'
        })
        self.assertNotIn('_auth_user_id', client.session)


# ============================================================
# TP03 - ESTUDIANTE NO ACCEDE AL CMS
# ============================================================
class StudentCannotAccessCMSTest(TestCase):
    """TP03: Un estudiante no puede acceder al CMS de instructores."""

    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user('student', password='pass123', is_staff=False)

    def test_student_cannot_access_manage_course_list(self):
        client = Client()
        client.force_login(self.student)
        response = client.get(reverse('manage_course_list'))
        self.assertIn(response.status_code, [302, 403, 404])

    def test_student_cannot_access_course_create(self):
        client = Client()
        client.force_login(self.student)
        response = client.get(reverse('course_create'))
        self.assertIn(response.status_code, [302, 403, 404])

    def test_anonymous_redirected_to_login(self):
        client = Client()
        response = client.get(reverse('manage_course_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)


# ============================================================
# TP04 - CONTENIDO POLIMÓRFICO
# ============================================================
class PolymorphicContentTest(TestCase):
    """TP04: Crear curso con contenido polimórfico (Text, Video, Image, File)."""

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(title='Test', slug='test')
        cls.instructor = User.objects.create_user('instructor', password='pass123', is_staff=True)
        cls.course = Course.objects.create(
            owner=cls.instructor, subject=cls.subject,
            title='Curso', slug='curso', overview='Test'
        )
        cls.module = Module.objects.create(course=cls.course, title='Módulo')

    def test_create_text_content(self):
        text = Text.objects.create(owner=self.instructor, title='Texto', content='Hola')
        content = Content.objects.create(module=self.module, item=text)
        self.assertEqual(content.item, text)
        self.assertIsInstance(content.item, Text)

    def test_create_video_content(self):
        video = Video.objects.create(
            owner=self.instructor, title='Video',
            url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        content = Content.objects.create(module=self.module, item=video)
        self.assertIsInstance(content.item, Video)

    def test_create_image_content(self):
        image = Image.objects.create(owner=self.instructor, title='Img', file='images/test.jpg')
        content = Content.objects.create(module=self.module, item=image)
        self.assertIsInstance(content.item, Image)

    def test_create_file_content(self):
        file_ = File.objects.create(owner=self.instructor, title='PDF', file='files/doc.pdf')
        content = Content.objects.create(module=self.module, item=file_)
        self.assertIsInstance(content.item, File)

    def test_mixed_content_in_same_module(self):
        text = Text.objects.create(owner=self.instructor, title='T', content='x')
        video = Video.objects.create(owner=self.instructor, title='V', url='https://youtu.be/x')
        Content.objects.create(module=self.module, item=text)
        Content.objects.create(module=self.module, item=video)
        self.assertEqual(Content.objects.filter(module=self.module).count(), 2)


# ============================================================
# TP05, TP06, TP07 - PRUEBAS MANUALES
# ============================================================
# Documentadas en anexo de pruebas manuales.


# ============================================================
# TP08 - DASHBOARD KPIs REALES
# ============================================================
class DashboardKPITest(TestCase):
    """TP08: El dashboard muestra KPIs reales."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass123')
        cls.subject = Subject.objects.create(title='Test Subject', slug='test-subject')
        cls.instructor = User.objects.create_user('instructor', password='testpass123', is_staff=True)
        cls.course = Course.objects.create(
            owner=cls.instructor, subject=cls.subject,
            title='Test Course', slug='test-course', overview='Test'
        )
        cls.student1 = User.objects.create_user('student1', password='pass123')
        cls.student2 = User.objects.create_user('student2', password='pass123')
        cls.course.students.add(cls.student1, cls.student2)

        cls.module = Module.objects.create(course=cls.course, title='Test Module')
        cls.quiz = Quiz.objects.create(
            module=cls.module, title='Test Quiz',
            passing_score=70, is_active=True
        )

        QuizAttempt.objects.create(
            student=cls.student1, quiz=cls.quiz,
            score=80, passed=True, completed_at=timezone.now()
        )
        QuizAttempt.objects.create(
            student=cls.student2, quiz=cls.quiz,
            score=60, passed=False, completed_at=timezone.now()
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.admin)

    def test_dashboard_accessible_by_admin(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_uses_correct_template(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertTemplateUsed(response, 'admin/dashboard_kpis.html')

    def test_total_alumnos_inscritos(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.context['total_alumnos_inscritos'], 2)

    def test_alumnos_finalizados(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.context['alumnos_finalizados'], 1)

    def test_promedio_notas(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.context['promedio_notas'], 70.0)

    def test_tasa_aprobacion(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.context['tasa_aprobacion'], 50.0)

    def test_total_cursos(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.context['total_cursos'], 1)

    def test_cursos_detalle_existe(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertIn('cursos_detalle', response.context)
        self.assertEqual(len(response.context['cursos_detalle']), 1)

    def test_cursos_detalle_es_queryset_de_courses(self):
        response = self.client.get('/admin/dashboard-kpis/')
        curso = response.context['cursos_detalle'][0]
        self.assertIsInstance(curso, Course)

    def test_cursos_detalle_valores_correctos(self):
        response = self.client.get('/admin/dashboard-kpis/')
        curso = response.context['cursos_detalle'][0]
        self.assertEqual(curso.title, 'Test Course')
        self.assertEqual(curso.total_inscritos, 2)
        self.assertEqual(curso.total_aprobados, 1)
        self.assertEqual(curso.promedio_nota, 70.0)

    def test_umbrales_presentes_en_contexto(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.context['umbral_meta_nota'], 70.0)
        self.assertEqual(response.context['umbral_meta_dias'], 14)

    def test_cumple_meta_notas_true_cuando_promedio_iguala_umbral(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertTrue(response.context['cumple_meta_notas'])

    def test_html_muestra_titulo_dashboard(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertContains(response, 'Dashboard de KPIs')
        self.assertContains(response, 'Total Alumnos Inscritos')
        self.assertContains(response, 'Alumnos que Finalizaron')

    def test_html_muestra_curso_en_tabla(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'Test Subject')

    def test_total_intentos_no_esta_en_contexto_hallazgo(self):
        """HALLAZGO: el template usa {{ total_intentos }} pero la vista no lo provee."""
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertNotIn('total_intentos', response.context)


# ============================================================
# TP09 - INDICADORES DE UMBRAL VERDE/ROJO
# ============================================================
class ThresholdIndicatorTest(TestCase):
    """TP09: Indicadores verde/rojo según umbral de aprobación."""

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(title='T', slug='t')
        cls.instructor = User.objects.create_user('i', password='p', is_staff=True)
        cls.student = User.objects.create_user('s', password='p')
        cls.course = Course.objects.create(
            owner=cls.instructor, subject=cls.subject,
            title='C', slug='c', overview='x'
        )
        cls.module = Module.objects.create(course=cls.course, title='M')
        cls.quiz = Quiz.objects.create(module=cls.module, title='Q', passing_score=70)

    def test_green_when_passed(self):
        attempt = QuizAttempt.objects.create(
            student=self.student, quiz=self.quiz,
            score=85, passed=True, completed_at=timezone.now()
        )
        self.assertEqual(attempt.threshold_color, 'green')

    def test_red_when_failed(self):
        attempt = QuizAttempt.objects.create(
            student=self.student, quiz=self.quiz,
            score=50, passed=False, completed_at=timezone.now()
        )
        self.assertEqual(attempt.threshold_color, 'red')

    def test_gray_when_no_score(self):
        attempt = QuizAttempt.objects.create(student=self.student, quiz=self.quiz)
        self.assertEqual(attempt.threshold_color, 'gray')

    def test_exactly_at_threshold_is_passed(self):
        attempt = QuizAttempt.objects.create(
            student=self.student, quiz=self.quiz,
            score=70, passed=True, completed_at=timezone.now()
        )
        self.assertTrue(attempt.passed)
        self.assertEqual(attempt.threshold_color, 'green')


# ============================================================
# TP09b - UMBRALES DEL DASHBOARD
# ============================================================
class DashboardThresholdTest(TestCase):
    """TP09b: El dashboard muestra indicadores verdes/rojos según umbrales."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass123')
        cls.subject = Subject.objects.create(title='T', slug='t')
        cls.instructor = User.objects.create_user('i', password='p', is_staff=True)
        cls.course = Course.objects.create(
            owner=cls.instructor, subject=cls.subject,
            title='C', slug='c', overview='x'
        )
        cls.student = User.objects.create_user('s', password='p')
        cls.course.students.add(cls.student)
        cls.module = Module.objects.create(course=cls.course, title='M')
        cls.quiz = Quiz.objects.create(module=cls.module, title='Q', passing_score=70)
        QuizAttempt.objects.create(
            student=cls.student, quiz=cls.quiz,
            score=85, passed=True, completed_at=timezone.now()
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.admin)

    def test_dashboard_shows_green_badge_when_above_threshold(self):
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertTrue(response.context['cumple_meta_notas'])
        self.assertContains(response, 'Cumple meta')

    def test_dashboard_shows_red_badge_when_below_threshold(self):
        QuizAttempt.objects.all().update(score=50, passed=False)
        response = self.client.get('/admin/dashboard-kpis/')
        self.assertFalse(response.context['cumple_meta_notas'])
        self.assertContains(response, 'Bajo la meta')


# ============================================================
# TP10 - DASHBOARD REQUIERE LOGIN
# ============================================================
class DashboardRequiresLoginTest(TestCase):
    """TP10: Un usuario no autenticado no puede ver el dashboard."""

    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user('student', password='pass123', is_staff=False)

    def test_anonymous_user_redirected_to_login(self):
        client = Client()
        response = client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_non_staff_user_cannot_access_dashboard(self):
        client = Client()
        client.force_login(self.student)
        response = client.get('/admin/dashboard-kpis/')
        self.assertEqual(response.status_code, 302)


# ============================================================
# TP11 - INSTRUCTOR NO VE PREGUNTAS AJENAS
# ============================================================
class QuestionAdminFilteringTest(TestCase):
    """TP11: El admin filtra preguntas por owner."""

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(title='T', slug='t')
        cls.instructor1 = User.objects.create_user('i1', password='p', is_staff=True)
        cls.instructor2 = User.objects.create_user('i2', password='p', is_staff=True)

        # Permisos de admin para que no redirija a login
        permissions = Permission.objects.filter(content_type__app_label='courses')
        cls.instructor1.user_permissions.add(*permissions)
        cls.instructor2.user_permissions.add(*permissions)

        cls.course1 = Course.objects.create(
            owner=cls.instructor1, subject=cls.subject,
            title='C1', slug='c1', overview='x'
        )
        cls.course2 = Course.objects.create(
            owner=cls.instructor2, subject=cls.subject,
            title='C2', slug='c2', overview='x'
        )
        cls.module1 = Module.objects.create(course=cls.course1, title='M1')
        cls.module2 = Module.objects.create(course=cls.course2, title='M2')
        cls.quiz1 = Quiz.objects.create(module=cls.module1, title='Q1')
        cls.quiz2 = Quiz.objects.create(module=cls.module2, title='Q2')

        cls.question1 = Question.objects.create(quiz=cls.quiz1, text='Pregunta de instructor 1')
        cls.question2 = Question.objects.create(quiz=cls.quiz2, text='Pregunta de instructor 2')

    def test_instructor1_sees_only_own_questions(self):
        client = Client()
        client.force_login(self.instructor1)
        response = client.get('/admin/courses/question/')
        self.assertContains(response, 'Pregunta de instructor 1')
        self.assertNotContains(response, 'Pregunta de instructor 2')

    def test_instructor2_sees_only_own_questions(self):
        client = Client()
        client.force_login(self.instructor2)
        response = client.get('/admin/courses/question/')
        self.assertContains(response, 'Pregunta de instructor 2')
        self.assertNotContains(response, 'Pregunta de instructor 1')


# ============================================================
# TP12 - INSTRUCTOR NO VE QUIZZES AJENOS
# ============================================================
class QuizAdminFilteringTest(TestCase):
    """TP12: El admin filtra quizzes por owner."""

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(title='T', slug='t')
        cls.instructor1 = User.objects.create_user('i1', password='p', is_staff=True)
        cls.instructor2 = User.objects.create_user('i2', password='p', is_staff=True)

        permissions = Permission.objects.filter(content_type__app_label='courses')
        cls.instructor1.user_permissions.add(*permissions)
        cls.instructor2.user_permissions.add(*permissions)

        cls.course1 = Course.objects.create(
            owner=cls.instructor1, subject=cls.subject,
            title='C1', slug='c1', overview='x'
        )
        cls.course2 = Course.objects.create(
            owner=cls.instructor2, subject=cls.subject,
            title='C2', slug='c2', overview='x'
        )
        cls.module1 = Module.objects.create(course=cls.course1, title='M1')
        cls.module2 = Module.objects.create(course=cls.course2, title='M2')

        cls.quiz1 = Quiz.objects.create(module=cls.module1, title='Quiz de instructor 1')
        cls.quiz2 = Quiz.objects.create(module=cls.module2, title='Quiz de instructor 2')

    def test_instructor1_sees_only_own_quizzes(self):
        client = Client()
        client.force_login(self.instructor1)
        response = client.get('/admin/courses/quiz/')
        self.assertContains(response, 'Quiz de instructor 1')
        self.assertNotContains(response, 'Quiz de instructor 2')


# ============================================================
# TP13 - INCONSISTENCIA EN CÁLCULO DE SCORE (HALLAZGO)
# ============================================================
class ScoreCalculationInconsistencyTest(TestCase):
    """
    TP13: Documenta que el modelo y la vista calculan el score distinto.
    - Modelo: por número de preguntas.
    - Vista: por puntos.
    """

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(title='T', slug='t')
        cls.instructor = User.objects.create_user('i', password='p', is_staff=True)
        cls.student = User.objects.create_user('s', password='p')
        cls.course = Course.objects.create(
            owner=cls.instructor, subject=cls.subject,
            title='C', slug='c', overview='x'
        )
        cls.course.students.add(cls.student)
        cls.module = Module.objects.create(course=cls.course, title='M')
        cls.quiz = Quiz.objects.create(module=cls.module, title='Q', passing_score=70, is_active=True)

        cls.q1 = Question.objects.create(quiz=cls.quiz, text='Q1', points=10)
        cls.q2 = Question.objects.create(quiz=cls.quiz, text='Q2', points=30)
        cls.q1_ok = Answer.objects.create(question=cls.q1, text='ok', is_correct=True)
        cls.q2_no = Answer.objects.create(question=cls.q2, text='no', is_correct=False)

    def test_model_calculates_by_questions(self):
        """El modelo cuenta preguntas correctas, ignorando puntos."""
        attempt = QuizAttempt.objects.create(student=self.student, quiz=self.quiz)
        StudentAnswer.objects.create(attempt=attempt, question=self.q1, selected_answer=self.q1_ok)
        StudentAnswer.objects.create(attempt=attempt, question=self.q2, selected_answer=self.q2_no)
        score = attempt.calculate_score()
        self.assertEqual(score, 50.0)

    def test_view_calculates_by_points(self):
        """La vista cuenta puntos, no preguntas."""
        client = Client()
        client.force_login(self.student)
        client.get(reverse('quiz_take', args=[self.quiz.id]))
        client.post(reverse('quiz_submit', args=[self.quiz.id]), {
            f'question_{self.q1.id}': self.q1_ok.id,
            f'question_{self.q2.id}': self.q2_no.id,
        })
        attempt = QuizAttempt.objects.get(student=self.student, quiz=self.quiz)
        self.assertEqual(attempt.score, 25.0)


# ============================================================
# TP14 - QUIZ_SUBMIT SIN INSCRIPCIÓN (HALLAZGO)
# ============================================================
class QuizSubmitWithoutEnrollmentTest(TestCase):
    """TP14: Documenta que quiz_submit no valida inscripción."""

    @classmethod
    def setUpTestData(cls):
        cls.subject = Subject.objects.create(title='T', slug='t')
        cls.instructor = User.objects.create_user('i', password='p', is_staff=True)
        cls.student = User.objects.create_user('s', password='p')
        cls.course = Course.objects.create(
            owner=cls.instructor, subject=cls.subject,
            title='C', slug='c', overview='x'
        )
        # ⚠️ NO inscribimos al estudiante
        cls.module = Module.objects.create(course=cls.course, title='M')
        cls.quiz = Quiz.objects.create(module=cls.module, title='Q', passing_score=70, is_active=True)
        cls.q1 = Question.objects.create(quiz=cls.quiz, text='Q1', points=10)
        cls.q1_ok = Answer.objects.create(question=cls.q1, text='ok', is_correct=True)

    def test_quiz_take_redirects_when_not_enrolled(self):
        """quiz_take SÍ valida inscripción."""
        client = Client()
        client.force_login(self.student)
        response = client.get(reverse('quiz_take', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('student_course_list'), response.url)

    def test_quiz_submit_does_not_validate_enrollment(self):
        """quiz_submit NO valida inscripción. Documentamos el hallazgo."""
        attempt = QuizAttempt.objects.create(student=self.student, quiz=self.quiz)
        client = Client()
        client.force_login(self.student)
        client.post(reverse('quiz_submit', args=[self.quiz.id]), {
            f'question_{self.q1.id}': self.q1_ok.id,
        })
        attempt.refresh_from_db()
        self.assertIsNotNone(attempt.completed_at)
        self.assertEqual(attempt.score, 100.0)