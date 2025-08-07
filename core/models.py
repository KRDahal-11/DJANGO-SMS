from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll_no = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"


class TeacherFeedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    teacher_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback for {self.student.name} by {self.teacher_name}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        if self.expires_at:
            return timezone.now() <= self.expires_at
        return True
    
