from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import File
import os
import openpyxl
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


class User(AbstractUser):
    role = models.TextField(max_length=40, null=False, default="student")
    username = models.TextField(max_length=40, null=True, default="user name")
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(upload_to="Images", null=True)
    phone = models.IntegerField(max_length=10, null=True)
    REQUIRED_FIELDS = ['email']


class Academic_info(models.Model):
    semester = models.TextField(max_length=8, null=False)
    branch = models.TextField(max_length=20, null=False, unique=True)

    def __str__(self):

        return f"{self.semester}" + f" {self.branch}"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    usn = models.TextField(max_length=30, null=False, unique=True)
    name = models.TextField(max_length=30, default="student_name", null=True)
    academic_info = models.ForeignKey(
        Academic_info, null=True, on_delete=models.CASCADE)

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
    designation = models.TextField(
        max_length=40, unique=False, default="no designation")

    def __str__(self):
        return f"{self.user.username}"


class Subject(models.Model):
    teacher = models.ForeignKey(
        teacher, null=True, on_delete=models.CASCADE)
    academic_info = models.ForeignKey(
        Academic_info, null=True, on_delete=models.CASCADE)
    subject_name = models.TextField(max_length=40, null=True)
    subject_code = models.TextField(max_length=40, null=False)
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

    # def save(self, *args, **kwargs):
    #     # and update file path
    #     pth = str(os.path.join(
    #         BASE_DIR, 'static\\media\\records\\somefile1.xlsx'))
    #     print("path", pth)
    #     f = openpyxl.load_workbook(pth)
    #     self.attendance_file.save(
    #         self.subject_code, File(f), save=False)
    #     super(Subject, self).save(*args, **kwargs)


class Class(models.Model):
    subject = models.ForeignKey(
        Subject, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Images", null=True)

    def __str__(self):
        return f"{self.id}"+f"_{self.subject.subject_code}"


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
