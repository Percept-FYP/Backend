from django.contrib import admin
from api.models import attendance, Student, teacher, Class, Parents, Subject, User, Academic_info

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(teacher)
admin.site.register(Parents)
admin.site.register(Class)
admin.site.register(attendance)
admin.site.register(User)
admin.site.register(Academic_info)
