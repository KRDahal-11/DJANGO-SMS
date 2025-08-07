
from django.shortcuts import render
from .models import Student, Event, TeacherFeedback, Notice
from .forms import StudentForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from core.models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db import models

def home(request):
    return render(request, 'core/home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/student_list.html', {'students': students})

def student_dashboard(request):
    """Enhanced student dashboard with calendar, feedback, and notices"""
    if not (request.user.is_authenticated and request.user.username.startswith("std_")):
        return HttpResponseForbidden("Unauthorized: Only student IDs starting with 'std_' can access this page.")
    # Get upcoming events (next 30 days)
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(
        date__gte=today,
        date__lte=today + timedelta(days=30)
    ).order_by('date', 'time')[:5]
    
    # Get active notices (not expired)
    today = timezone.now()
    active_notices = Notice.objects.filter(
        models.Q(expires_at__isnull=True) | models.Q(expires_at__gte=today)
    ).order_by('-created_at')[:3]
    
    # Get teacher feedback for the current student (if logged in as student)
    teacher_feedbacks = []
    if request.user.is_authenticated and not request.user.username.startswith("teacher_"):
        try:
            student = Student.objects.get(user=request.user)
            teacher_feedbacks = TeacherFeedback.objects.filter(student=student).order_by('-created_at')[:3]
        except Student.DoesNotExist:
            pass
    
    context = {
        'upcoming_events': upcoming_events,
        'active_notices': active_notices,
        'teacher_feedbacks': teacher_feedbacks,
        'today': today,
    }
    
    return render(request, 'core/student_dashboard.html', context)

def edit_student(request, pk):
    if not request.user.username.startswith("teacher_"):
        return HttpResponseForbidden("Unauthorized access")

    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'core/edit_student.html', {'form': form})

def add_student(request):
    if not request.user.username.startswith("teacher_"):
        return HttpResponseForbidden("Unauthorized access")

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'core/edit_student.html', {'form': form})


# for signing up a new user
def signup(request):
    if request.method == 'POST':
        user=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')

        if password1 != password2:
            return render(request, 'core/signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=user).exists():
            return render(request, 'core/signup.html', {'error': 'Username already exists'})
        
        try:
            print(user, email, password2)
            # Create a new user
            new_user = User.objects.create_user(username=user, password=password2, email=email)
            new_user.save()
            # Optionally, redirect to a success page or login page
            return redirect('/login')
        except Exception as e:
            print(f"Error creating user: {e}")
            return render(request, 'core/signup.html', {'error': 'An error occurred while creating the account'})
    else:
        return render(request, 'core/signup.html')
    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect based on user type
            if username.startswith('std_'):
                return redirect('/student-dashboard')
            elif username.startswith('teach_'):
                return redirect('/teacher-dashboard')
            else:
                return render(request, 'core/login.html', {'error': 'Unknown user type. Contact admin.'})
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')


def logout(request):
    auth_logout(request)
    return redirect('/')

def teacher_dashboard(request):
    """Teacher dashboard with event calendar (starter)"""
    if not (request.user.is_authenticated and request.user.username.startswith("teach_")):
        return HttpResponseForbidden("Unauthorized: Only teacher IDs starting with 'teach_' can access this page.")
    
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Get all events for the current month
    from datetime import date
    first_day = date(current_year, current_month, 1)
    if current_month == 12:
        last_day = date(current_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(current_year, current_month + 1, 1) - timedelta(days=1)
    
    month_events = Event.objects.filter(
        date__gte=first_day,
        date__lte=last_day
    ).order_by('date', 'time')
    
    # Get upcoming events (next 30 days) for the sidebar
    upcoming_events = Event.objects.filter(
        date__gte=today,
        date__lte=today + timedelta(days=30)
    ).order_by('date', 'time')[:10]
    
    # Create calendar data
    import calendar
    cal = calendar.monthcalendar(current_year, current_month)
    month_name = calendar.month_name[current_month]
    
    context = {
        'upcoming_events': upcoming_events,
        'month_events': month_events,
        'calendar': cal,
        'month_name': month_name,
        'current_year': current_year,
        'current_month': current_month,
        'today': today,
        'first_day': first_day,
        'last_day': last_day,
    }
    return render(request, 'core/teacher_dashboard.html', context)



