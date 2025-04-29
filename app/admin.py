from django.contrib import admin
from app.models import *

admin.site.register([User, Departments, Course, Teacher, Student, Parents, GroupStudent, Table, Rooms, TableType, Day])
# Register your models here.
