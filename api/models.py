from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    role = models.TextField(max_length=40, null=False, default="student")
    username = models.TextField(max_length=40, null=True, default="user name")
    email = models.EmailField(_('email address'), unique=True)
    phone = models.IntegerField(max_length=10, null=True)
    REQUIRED_FIELDS = ['email']


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    usn = models.TextField(max_length=30, null=False, unique=True)
    name = models.TextField(max_length=30, default="student_name", null=True)

    def __str__(self):
        return f"{self.usn}"


class Parents(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, null=False, primary_key=True)
    name = models.TextField(max_length=30, default="student_name", null=True)

    def __str__(self):
        return f"{self.student.usn}"


class teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    designation = models.TextField(max_length=40, unique=False)

    def __str__(self):
        return f"{self.user.username}"


class Subject(models.Model):
    teacher = models.ForeignKey(
        teacher, null=True, on_delete=models.CASCADE)
    subject_name = models.TextField(max_length=40, null=True)
    subject_code = models.TextField(max_length=40, null=False)

    def __str__(self):
        return f"{self.subject_code}"


class Class(models.Model):
    subject = models.ForeignKey(
        Subject, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Images", null=True)

    def __str__(self):
        return f"{self.subject.subject_code}"


class attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attend = models.TextField(max_length=30, default="absent", null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    Class = models.ForeignKey(Class, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.student.usn}"


class info(models.Model):
    image = models.ImageField(upload_to="Images", null=True)
    class_name = models.TextField(max_length=30, null=False)
    teacher = models.TextField(max_length=30, null=False)
