from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Course, StudentRegistration, Student,CourseSchedule,CourseReport
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import CourseSchedule
from django.contrib import messages
from .models import Reminder
from django.utils import timezone
from .models import Reminder
from django.core.mail import send_mail
from .forms import EmailChangeForm
from .forms import FirstNameChangeForm, LastNameChangeForm
from .models import Notification



def home(request):
    return render(request, 'registration/home.html')

@login_required
def search_courses(request):
    query = request.GET.get('query', '')
    if query:
        courses = Course.objects.filter(name__icontains=query)
    else:
        courses = Course.objects.all()

    no_results = not courses.exists()
    
    return render(request, 'registration/search_courses.html', {'courses': courses, 'query': query, 'no_results': no_results})

@login_required
def view_course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'registration/course_details.html', {'course': course})

@login_required
def add_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        prerequisites = course.prerequisites.all()
        completed_courses = StudentRegistration.objects.filter(student=student).values_list('course', flat=True)
        for prereq in prerequisites:
            if prereq.prerequisite_course.id not in completed_courses:
                messages.error(request, f'You have not completed the prerequisite: {prereq.prerequisite_course.name}')
                return render(request, 'registration/course_details.html', {'course': course, 'error': 'You have not completed the prerequisites'})

        student_courses = StudentRegistration.objects.filter(student=student).select_related('course__schedule')
        for student_course in student_courses:
            if student_course.course.schedule == course.schedule:
                messages.error(request, 'This course conflicts with your current schedule.')
                return render(request, 'registration/course_details.html', {'course': course, 'error': 'Schedule conflict'})

        StudentRegistration.objects.create(student=student, course=course)
        messages.success(request, 'Course added to your schedule successfully.')
        return redirect('view_schedule')

    return render(request, 'registration/course_details.html', {'course': course})

@login_required
def view_schedule(request):
    try:
        student = Student.objects.get(user=request.user)
        registrations = StudentRegistration.objects.filter(student=student)
        courses = [registration.course for registration in registrations]
        return render(request, 'registration/schedule.html', {'course_schedules': courses})
    except Student.DoesNotExist:
        messages.error(request, 'No student record found for the current user.')
        return redirect('home') 

@login_required
def profile(request):
     reminders = Reminder.objects.filter(user=request.user)
     return render(request, 'registration/profile.html', {
        'reminders': reminders,
    })
@login_required
def settings(request):
    return render(request, 'registration/settings.html')



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
    else:
        return render(request, 'registration/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')
def reminders(request):
    user_reminders = Reminder.objects.filter(user=request.user)
    return render(request, 'registration/reminders.html', {'reminders': user_reminders})

def notification(request):
    mynotification = Notification.objects.filter(sender=request.user)
    return render(request, 'registration/notification.html', {'notifications': mynotification})


def course_reports(request):
    reports = CourseReport.objects.all()
    return render(request, 'registration/course_reports.html', {'reports': reports})

def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['new_email']
            user.username = user.email
            user.save()
            return redirect('settings')
    else:
        form = EmailChangeForm(instance=request.user)
    return render(request, 'registration/email_change.html', {'form': form})


def first_name_change(request):
    if request.method == 'POST':
        form = FirstNameChangeForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.save()
            return redirect('settings')
    else:
        form = FirstNameChangeForm()
    return render(request, 'registration/first_name_change.html', {'form': form})

def last_name_change(request):
    if request.method == 'POST':
        form = LastNameChangeForm(request.POST)
        if form.is_valid():
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            return redirect('settings')
    else:
        form = LastNameChangeForm()
    return render(request, 'registration/last_name_change.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
    registration = StudentRegistration.objects.filter(student=student, course=course)
    registration.delete()
    return redirect('view_schedule')