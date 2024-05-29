from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _


class CourseSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_no = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.days} {self.start_time}-{self.end_time} in {self.room_no}'

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    capacity = models.IntegerField()
    schedule = models.ForeignKey('CourseSchedule', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} - {self.name}'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128,default='defaultpassword')

    def __str__(self):
        return self.name

class StudentRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.name} - {self.course.name}'

class Prerequisite(models.Model):
    course = models.ForeignKey('Course', related_name='prerequisite_for', on_delete=models.CASCADE)
    prerequisite_course = models.ForeignKey('Course', related_name='prerequisites', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.prerequisite_course.name} is a prerequisite for {self.course.name}"
    
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_type = models.CharField(max_length=100)
    reminder_date = models.DateTimeField()

    def __str__(self):
        return f"{self.reminder_type} for {self.user.username} on {self.reminder_date}"
    

class CourseReport(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    report_date = models.DateField()
    registration_count = models.IntegerField(default=0)
    popularity_score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.course} Report - {self.report_date}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mynotification')
    notification_type = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.user.username} - {self.notification_type} - {self.date}'