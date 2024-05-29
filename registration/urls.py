from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search_courses, name='search_courses'),
    path('course/<int:course_id>/', views.view_course_details, name='view_course_details'),
    path('course/<int:course_id>/add/', views.add_course, name='add_course'),
    path('schedule/', views.view_schedule, name='view_schedule'),
    path('accounts/profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('addcourse/', views.add_course, name='addcourse'),
    path('reminders/', views.reminders, name='reminders'),
    path('reports/', views.course_reports, name='course_reports'),
    path('email_change/', views.email_change, name='email_change'),
    path('first_name_change/', views.first_name_change, name='first_name_change'),
    path('last_name_change/', views.last_name_change, name='last_name_change'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('notification/', views.notification, name='notification'),
    path('profile/', views.profile, name='profile'),







    
    
]
