from django.db import models


class attendance(models.Model):
    usn = models.TextField(max_length=30, null=False)
    attend = models.TextField(max_length=30, default="absent", null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    class_id = models.TextField(max_length=30, default="null", null=False)


class Student(models.Model):
    usn = models.TextField(max_length=30, null=False)
    name = models.TextField(max_length=30, default="student_name", null=True)

class info(models.Model):
    image = models.ImageField(upload_to="Images", null=True)
    class_name = models.TextField(max_length=30, null=False)
    teacher = models.TextField(max_length=30, null=False)
    