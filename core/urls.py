from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add/', views.add_student, name='add_student'),
    path('<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]