from django.contrib import admin
from .models import Student, Event, TeacherFeedback, Notice

admin.site.register(Student)
admin.site.register(Event)
admin.site.register(TeacherFeedback)
admin.site.register(Notice)