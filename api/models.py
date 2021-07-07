from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import File
import os
import openpyxl
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


class User(AbstractUser):
    role = models.CharField(max_length=40, null=False, default="student")
    username = models.CharField(max_length=40, null=True, default="user name")
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(upload_to="Images", null=True)
    phone = models.IntegerField(null=True)
    REQUIRED_FIELDS = ['email']


class Academic_info(models.Model):
    semester = models.CharField(max_length=20, null=False, unique=True)
    branch = models.CharField(max_length=60, null=False, unique=True)
    scheme = models.IntegerField(null=True)

    class meta:
        unique_together = [['semester', 'branch']]

    def __str__(self):

        return f"{self.semester}" + f" {self.branch}"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    usn = models.CharField(max_length=40, null=False, unique=True)
    name = models.CharField(max_length=40, default="student_name", null=True)
    academic_info = models.ForeignKey(
        Academic_info, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usn}"


class Parents(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, null=False, primary_key=True)
    name = models.CharField(max_length=40, default="student_name", null=True)

    def __str__(self):
        return f"{self.student.usn}"


class teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    designation = models.CharField(
        max_length=40, unique=False, default="no designation")

    def __str__(self):
        return f"{self.user.username}"


class Subject(models.Model):
    teacher = models.ForeignKey(
        teacher, null=True, on_delete=models.CASCADE)
    academic_info = models.ForeignKey(
        Academic_info, null=True, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=40, null=True)
    subject_code = models.CharField(max_length=40, null=False, unique=True)
    attendance_file = models.FileField(
        upload_to="records", null=True, default='records/somefile1.xlsx')

    def __str__(self):
        return f"{self.subject_code}"

    @property
    def fileURL(self):
        try:
            url = self.attendance_file.url
        except:
            url = ''
        return url


class Class(models.Model):
    subject = models.ForeignKey(
        Subject, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Images", null=True)

    def __str__(self):
        return f"{self.id}"+f"_{self.subject.subject_code}"


class attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attend = models.CharField(max_length=40, default="absent", null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    Class = models.ForeignKey(Class, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.student.usn}"
