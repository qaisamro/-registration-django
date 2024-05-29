from django.contrib import admin
from.models import CourseSchedule
from.models import Course
from.models import Student
from.models import StudentRegistration
from .models import Prerequisite
from .models import Reminder
from .models import CourseReport
from .models import Notification



# Register your models here.
admin.site.register(CourseSchedule)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(StudentRegistration)
admin.site.register(Prerequisite)
admin.site.register(Reminder)
admin.site.register(CourseReport)
admin.site.register(Notification)


