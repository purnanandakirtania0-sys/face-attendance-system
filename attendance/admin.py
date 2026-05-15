from django.contrib import admin
from .models import *

from .models import Student
from .models import Attendance

admin.site.site_header = "Face Attendance Admin"
admin.site.site_title = "Face Attendance"
admin.site.index_title = "Welcome Admin"

admin.site.register(Student)

admin.site.register(Attendance)
