from django.contrib import admin
from api.models import attendance, Student, info, teacher, Class, Parents,Subject

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(teacher)
admin.site.register(Parents)
admin.site.register(Class)
admin.site.register(info)
admin.site.register(attendance)
