from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import include, path

from courses.views import CourseListView
from courses.admin_dashboard import DashboardAdminSite

# Reemplaza el admin site por defecto con el personalizado
admin.site.__class__ = DashboardAdminSite

# ---Vista inteligente de redirección post-login ---
@login_required
def smart_login_redirect(request):
    # Si es administrador o pertenece al grupo 'Instructors'
    if request.user.is_staff or request.user.groups.filter(name='Instructors').exists():
        return redirect('manage_course_list') # Va al CMS de instructores
    # Si es un estudiante (bombero) normal
    return redirect('student_course_list') # Va a "Mis cursos"
# -----------------------------------------------------------

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    path('students/', include('students.urls')),
    # --- Ruta para el redireccionamiento inteligente ---
    path('login-redirect/', smart_login_redirect, name='smart_login_redirect'),
    path('', CourseListView.as_view(), name='course_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)