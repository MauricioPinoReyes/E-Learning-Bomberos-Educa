from django.urls import path
from . import views

urlpatterns = [
    path(
        'register/',
        views.StudentRegistrationView.as_view(),
        name='student_registration'
    ),
    path(
        'enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'
    ),
    path(
        'courses/',
        views.StudentCourseListView.as_view(),
        name='student_course_list'
    ),
    path(
        'course/<pk>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail'
    ),
    path(
        'course/<pk>/<module_id>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail_module'
    ),

    # URLs de evaluaciones
    path('quiz/<int:quiz_id>/take/', views.quiz_take_view, name='quiz_take'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit_view, name='quiz_submit'),
    path('quiz/<int:quiz_id>/result/<int:attempt_id>/', views.quiz_result_view, name='quiz_result'),
]
    
